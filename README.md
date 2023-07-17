To run this project

1) Clone this repository

2) Download the latest version of Docker

3) Navigate to the root directory of this project
  
5) Generate the valid SSL certificates using:
    openssl req -x509 -nodes -newkey rsa:4096 -keyout ca.key -out ca.pem \
              -subj /O=me

6) Run docker-compose up

7) The recommendation service will be available at localhost:443 (to clients with the valid CA certificate generated in step 5) and the marketplace service will be available through REST at localhost:5001.
