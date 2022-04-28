# tis_form_bootstrap

This is all code relating to the "API" task of the TIS tech test. Included are the following:

* "index.html", which is a landing page including a custom-built "contact us" form built with Bootstrap 5.1 (adapted from the "Sign-in" custom component at https://getbootstrap.com/docs/5.1/examples )
* "thankyou.html", which is a simple thank you page for redirection after a form submission has passed both frontend (via Bootstrap) and backend (via AWS Lambda custom code and built-in HS Forms API) validation and has been persisted in the CRM.
* "lambda_function.py", which is the function code of a simple AWS Lambda function. I am using using the new built-in HTTPS Endpoint feature to expose it to a CORS-enabled GET request (https://aws.amazon.com/blogs/aws/announcing-aws-lambda-function-urls-built-in-https-endpoints-for-single-function-microservices/ ). It accepts the form submission, applies some (mostly dummy) validation to it, and then sends it to the HubSpot Forms API
