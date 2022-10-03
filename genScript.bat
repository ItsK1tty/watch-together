mkdir root-ca
cd root-ca
mkdir certs
mkdir crl
mkdir csr
mkdir newcerts
mkdir private

cd ..

mkdir sub-ca
cd sub-ca
mkdir certs
mkdir crl
mkdir csr
mkdir newcerts
mkdir private

cd ..

mkdir server-ca
cd server-ca
mkdir certs
mkdir crl
mkdir csr
mkdir newcerts
mkdir private

cd ..

echo

openssl rand -hex 16 > root-ca/serial
openssl rand -hex 16 > sub-ca/serial

openssl req -new -newkey rsa:4096 -days 1825 -nodes -x509 -subj "/CN=localhost" -keyout server-ca/server.key -out server-ca/server.crt
openssl x509 -text -in server-ca/server.crt -noout

openssl genrsa -aes256 -out root-ca/private/ca.key 4096
openssl genrsa -aes256 -out sub-ca/private/sub-ca.key 4096
openssl genrsa -out server-ca/private/server.key 2048

echo  > root-ca/root-ca.conf
echo nul > root-ca/index

pause

openssl req -config root-ca/root-ca.conf -key root-ca/private/ca.key -new -x509 -days 1825 -sha256 -extensions v3_ca -out root-ca/certs/ca.crt
openssl x509 -noout -in root-ca/certs/ca.crt -text

echo  > sub-ca/sub-ca.conf

pause

openssl req -config sub-ca/sub-ca.conf -new -key sub-ca/private/sub-ca.key -sha256 -out sub-ca/csr/sub-ca.csr
openssl ca -config root-ca/root-ca.conf -extensions v3_intermediate_ca -days 3650 -in sub-ca/csr/sub-ca.csr -out sub-ca/certs/sub-ca.crt
@REM здесь почему-то не пашет. может, это? http://www.ipsec-howto.org/x595.html

openssl x509 -noout -text -in sub-ca/certs/sub-ca.crt

openssl req -key server-ca/private/server.key -new -sha256 -out server-ca/csr/server.csr

openssl ca -config sub-ca/sub-ca.conf -extensions server_cert -days 1825 -notext -in server-ca/csr/server.csr -out server-ca/certs/server.crt
type server.crt sub-ca\certs\sub-ca.crt > server-ca/certs/chained.crt

