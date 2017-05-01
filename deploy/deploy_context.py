from fabric.api import env


env.use_ssh_config = True
ALLOWED_ENVIRONMENTS = ["dev", "stage", "prod"]


def validate_environment():
    enviro = env.enviro

    confirm = raw_input("Performing the deployment for [{enviro}]. Confirm the environment by typing it again: ".format(enviro = enviro))

    if enviro not in ALLOWED_ENVIRONMENTS or enviro != confirm:
        raise Exception("Not an allowed environment")


def confirm_hosts():
    print("This operation will affect {hosts}".format(hosts = env.hosts))
    input = raw_input("If this is correct, type 'confirm' : ")
    if input != "confirm":
        raise Exception("User exited")

validate_environment()

if env.enviro == "dev":
    IMAGE_ENGINE_TEMPLATE_URL = "http://ie.dev.trafficland.com/{publicId}/{size}?system={system}&pubtoken={" \
                              "pubtoken}&refreshRate={refreshRate} "
    DEBUG_LEVEL = "DEBUG"

if env.enviro == "stage":
    IMAGE_ENGINE_TEMPLATE_URL = "http://ie.stage.trafficland.com/{publicId}/{size}?system={system}&pubtoken={" \
                              "pubtoken}&refreshRate={refreshRate} "
    DEBUG_LEVEL = "DEBUG"

if env.enviro == "prod":
    IMAGE_ENGINE_TEMPLATE_URL = "http://ie.trafficland.com/{publicId}/{size}?system={system}&pubtoken={" \
                              "pubtoken}&refreshRate={refreshRate} "
    DEBUG_LEVEL = "INFO"

confirm_hosts()
