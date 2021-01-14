#
docker bulid -t hast21-image .

docker run --name hast21-container -p 80:80 hast21-image
