def api():
    print("\nhealth:","\n  curl --request GET \
     \n --url https://api.3vidence.com/auth/health")

    print("\nhjws:","\n  curl --request GET \
    \n  --url https://api.3vidence.com//htsp/hjws/YOUR_ID_HWJS")

    print("\nhjws-del","curl --request DELETE \
    \n  --url https://api.3vidence.com//htsp/hjws \
    \n  --header 'content-type: application/json' \
    \n  --data '{\"api_key\": \"YOUR_APIKEY\", \"id_hjws\":\"YOUR_ID_HWJS\"}'")

    print("\nhtsq: ","\n    curl --request POST --url https://api.3vidence.com/htsp/htsq \
    \n  --header 'content-type: application/json'\
    \n  --data '{ \"api_key\": \"YOUR_APIKEY\", \"algorithm\":\"YOUR_ALG_HASH\",\"hash\":\"YOUR_HASH\", \"cloud\": BOOLEAN, \"desc\": \"YOUR_DESCRIPTION\"}'")

    print("\nhtsq-a:","\n    curl --request POST \
    \n  --url https://api.3vidence.com//htsp/branch/projectmayhem \
    \n  --header 'content-type: application/json' \
    \n    --data '{\"branch\": \"YOUR_BRANCH\"}'")

    print("\nhtsr:","\n curl --request POST \
    \n  --url https://api.3vidence.com//htsp/htsr \
    \n  --header 'content-type: application/json' \
    \n  --data '{\"hjws\": \"YOUR_HJWS\",\"kid\": \"YOUR_KID\"}'")

    print("\nhtsr-c:","\n  curl --request GET \
    \n  --url https://api.3vidence.com//htsp/hjws/YOUR_ID_HWJS")

    print("\ninfo:", "\n   curl --request GET \
    \n  --url https://api.3vidence.com//htsp/info \
    \n  --header 'authorization: YOUR_JWT'")

    print ("\ninfo_apikey:", "\n  curl --request POST \
    \n  --url https://api.3vidence.com//htsp/info/apikey \
    \n  --header 'content-type: application/json' \
    \n  --data '{ \"api_key\": \"YOUR_APIKEY\"}'")

    print("\npubkey:","\n   curl --request GET \
    \n  --url https://api.3vidence.com//htsp/pubkey/YOUR_KID")
