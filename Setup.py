from cx_Freeze import setup , Executable 

setup (
    name = "DecouvreTonClient_",
    version = "0.1",
    description ="OK",
    executables = [Executable("Interface.py")]
)