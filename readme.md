to install and run:

    pip3 install -r requirements.txt
    pytest


or

    docker build -t tests
    docker run tests

to extract allure resources

    docker cp $(docker ps -a -q | head -1):/usr/tests/alluredir .
then

    allure serve alluredir  