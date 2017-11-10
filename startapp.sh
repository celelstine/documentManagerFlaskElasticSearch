#!/usr/bin/env SHELL

function activate_env() {
    # function to activate the virtual environment
    echo "Activate a virtual environment at $1"
    echo "Activate a virtual environment at $1" >> startScript.log

    source $1 >> startScript.log

    if [ $? -ne 0 ]
    then
        echo 'error occurred while activating a virtual environment'
        exit 1
    fi
}

function install_virtualenv() {
    # function to install python virtualenv

    env_folder=${1}
    python_version=${2}

    echo "Installing virtualenv with ${python_version}"
    echo "Installing virtualenv with ${python_version}" >> startScript.log

    ${python_version} -m pip install ${virtualenv} >> startScript.log

    if [ $? -ne 0 ]
    then
        echo "An error occurred while installing virtualenv with ${python_version}"
        echo "An error occurred while installing virtualenv with ${python_version}" >> startScript.log
        exit 1
    else
        create_env ${env_folder}
    fi
}

function create_env() {
    # function to create a python virtual environment

    echo 'Should I setup the virtual environment in python2?'
    echo 'y=yes, n=no, any other answer = yes'
    read python_version

    if [ "${python_version}" == "n" ]  || [ "${python_version}" == "no" ]
    then
        python_version='python3'
    else
        python_version='python2'
    fi

    env_folder=$1

    echo "Create a virtual environment with ${python_version} at ${env_folder}"
    echo "Create a virtual environment with ${python_version} at ${env_folder}" >> startScript.log

    virtualenv --python=${python_version} ${env_folder}  >> startScript.log
    if [ $? -ne 0 ]
    then
        echo 'An error occurred while creating a virtual environment, we would install the python virtualenv and get back to you.'
        install_virtualenv ${env_folder} ${python_version}
    fi
}

function install_dependencies() {
    # function to install dependencies
    echo "Which file contains the project dependencies, 'requirements.txt', Right. Enter a file full name or press enter"
    read requirement_file

    if [${requirement_file} -eq '']; then
        requirement_file="requirements.txt"
    fi

    echo 'Installing project dependencies'
    echo 'Installing project dependencies' >> startScript.log
    pip install -r  ${requirement_file} >> startScript.log

    if [ $? -ne 0 ]; then
        echo 'Unable to install project dependencies'
        echo 'Unable to install project dependencies' >> startScript.log
        exit 1
    fi
}

function run_flaskApp() {
    # function to export the flask app
    echo 'What is the name of your flask main file'
    read flask_app

    flask_app_path=`find . -name $flask_app | head -n 1`

    if [ $? -ne 0 ]
    then
        echo 'Unable to excute the find command '
        echo 'Unable to excute the find command ' >> startScript.log
        exit
    else
        if  [ -f ${flask_app_path} ]
        then
            install_dependencies

            export FLASK_APP=${flask_app_path}
            python -m flask run

            if [ $? -ne 0 ]; then
                echo 'App is running'
            else
                echo 'Unable to run App'
                exit 1
            fi
        else
            echo 'Can not find the flask main file'
            echo 'Can not find the flask main file' >> startScript.log
            exit 1
        fi
    fi
}

function start() {
    #  function to start the app
    envpath=`find . -name 'activate' | head -n 1`

    if [ $? -ne 0 ]
    then
        echo 'Unable to excute the find command '
        echo 'Unable to excute the find command ' >> startScript.log
    else
        if  [ -z "$envpath"] || [ ! -f ${envpath} ]
        then
            echo "${envpath} is not a file"
            echo 'You do not not have a virtual environment, we need to create one.'
            echo 'Which folder should we store the virtual environment, venv; Right. Enter a folder or press enter'
            read env_folder

            if [ -z "$envpath"]
            then
                env_folder='venv'
            fi

            create_env ${env_folder}

            envpath="./${env_folder}/bin/activate"
        fi
    fi

    activate_env $envpath

    run_flaskApp
}

start