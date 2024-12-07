import platform

open_command = {
    "Windows": "code",
    "Darwin": "code",
    "Linux": "code"
}[platform.system()]

Program = ["py", "java", "cpp", "cs", "js", "css"]