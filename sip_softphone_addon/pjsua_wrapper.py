import pjsua2 as pj
import time
import logging
import threading

logger = logging.getLogger(__name__)

class Call(pj.Call):
    """
    High level Python Call object, derived from pjsua2's Call object.
    """
    def __init__(self, acc, call_id=pj.PJSUA_INVALID_ID):
        pj.Call.__init__(self, acc, call_id)
        self.connected = False

    def onCallState(self, prm):
        ci = self.getInfo()
        logger.info(f"Call state: {ci.stateText} (remote: {ci.remoteUri})")
        
        if ci.state == pj.PJSIP_INV_STATE_CONFIRMED:
            self.connected = True
            logger.info("Call connected!")
        elif ci.state == pj.PJSIP_INV_STATE_DISCONNECTED:
            self.connected = False
            logger.info("Call disconnected")

    def onCallMediaState(self, prm):
        ci = self.getInfo()
        for mi in ci.media:
            if mi.type == pj.PJMEDIA_TYPE_AUDIO and mi.status == pj.PJSUA_CALL_MEDIA_ACTIVE:
                am = self.getAudioMedia(mi.index)
                ep = pj.Endpoint.instance()
                ep.audDevManager().getCaptureDevMedia().startTransmit(am)
                am.startTransmit(ep.audDevManager().getPlaybackDevMedia())
                logger.info("Media started")


class Account(pj.Account):
    """
    High level Python Account object, derived from pjsua2's Account object.
    """
    def __init__(self):
        pj.Account.__init__(self)
        self.current_call = None

    def onRegState(self, prm):
        ai = self.getInfo()
        logger.info(f"Registration status: {ai.regStatusText} (code: {ai.regStatus})")

    def onIncomingCall(self, prm):
        c = Call(self, prm.callId)
        ci = c.getInfo()
        logger.info(f"Incoming call from {ci.remoteUri}")
        
        # Auto answer
        call_prm = pj.CallOpParam()
        call_prm.statusCode = 200
        c.answer(call_prm)
        self.current_call = c


class SIPSoftphone:
    def __init__(self, server, username, password, port=5060):
        self.server = server
        self.username = username
        self.password = password
        self.port = port
        self.ep = None
        self.account = None
        self.running = False
        self.thread = None

    def start(self):
        """Start the SIP softphone"""
        try:
            # Create endpoint
            self.ep = pj.Endpoint()
            self.ep.libCreate()

            # Initialize endpoint
            ep_cfg = pj.EpConfig()
            ep_cfg.logConfig.level = 4
            ep_cfg.logConfig.consoleLevel = 4
            self.ep.libInit(ep_cfg)

            # Create transport
            sipTpConfig = pj.TransportConfig()
            sipTpConfig.port = self.port
            self.ep.transportCreate(pj.PJSIP_TRANSPORT_UDP, sipTpConfig)

            # Start endpoint
            self.ep.libStart()

            # Create account
            acc_cfg = pj.AccountConfig()
            acc_cfg.idUri = f"sip:{self.username}@{self.server}"
            acc_cfg.regConfig.registrarUri = f"sip:{self.server}"
            
            cred = pj.AuthCredInfo("digest", "*", self.username, 0, self.password)
            acc_cfg.sipConfig.authCreds.append(cred)

            # Create account
            self.account = Account()
            self.account.create(acc_cfg)

            logger.info(f"SIP account created: {self.username}@{self.server}")
            self.running = True

            # Keep the thread alive
            self.thread = threading.Thread(target=self._keep_alive, daemon=True)
            self.thread.start()

            return True

        except Exception as e:
            logger.error(f"Failed to start SIP softphone: {e}")
            return False

    def _keep_alive(self):
        """Keep the SIP session alive"""
        while self.running:
            time.sleep(1)

    def make_call(self, destination):
        """Make an outgoing call"""
        try:
            if not self.account:
                logger.error("Account not created")
                return None

            call = Call(self.account)
            call_prm = pj.CallOpParam(True)
            
            dest_uri = f"sip:{destination}@{self.server}"
            call.makeCall(dest_uri, call_prm)
            
            logger.info(f"Making call to {dest_uri}")
            return call

        except Exception as e:
            logger.error(f"Failed to make call: {e}")
            return None

    def hangup_all(self):
        """Hang up all active calls"""
        try:
            if self.account and self.account.current_call:
                self.account.current_call.hangup(pj.CallOpParam())
                logger.info("Call hung up")
        except Exception as e:
            logger.error(f"Failed to hangup: {e}")

    def stop(self):
        """Stop the SIP softphone"""
        try:
            self.running = False
            if self.thread:
                self.thread.join(timeout=2)
            
            if self.account:
                self.account.shutdown()
            
            if self.ep:
                self.ep.libDestroy()
            
            logger.info("SIP softphone stopped")
        except Exception as e:
            logger.error(f"Error stopping softphone: {e}")
