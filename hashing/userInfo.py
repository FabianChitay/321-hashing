
class UserInfo:

    def __init__(self, user, algorithm, workFactor, salt, hash, userStr):
        self.user = user
        self.algorithm = algorithm
        self.workFactor = workFactor
        self.salt = salt
        self.hash = hash
        self.userStr = userStr
        self.password = ""

    def __str__(self):
        return f"""user: {self.user},
        algorithm: {self.algorithm},
        workfactor: {self.workFactor},
        salt: {self.salt},
        hash: {self.hash},
        userstr: {self.userStr},
        password: {self.password}
        """



