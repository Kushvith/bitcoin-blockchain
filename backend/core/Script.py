class Script:
    def __init__(self,cmds= None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds
            
    @classmethod
    def p2pkh_script(cls,h160):
        """takes h160 and returns the p2pkg scriptpubkey"""
        return Script([0x76,0xa9,h160,0x88,0xac])