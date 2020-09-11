def api():
    print("\nhealth:","\n  curl --request GET \
     \n --url https://api.3vidence.com/auth/health")

    print("\nlogin:", "\n  curl --request POST \
    \n  --url https://api.3vidence.com/auth/login \
    \n  --header 'content-type: application/json'\
    \n  --data '{\"email\": \"YOUR_EMAIL\" ,\"password\": \"YOUR_PASSWORD\"}'")
