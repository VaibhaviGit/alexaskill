# alexaskill

This project smart shopping is all about connecting Alexa with local groccery and medicine shops. User can get list of nearby stores, get list of available items and respective price list. User can also order items with voice command only.

The Smart shopping Alexa skill has 2 major components
1. SmartShopping.Json
	This file defines all the endpoints and the samples by which user interacts with Alexa
2. lambda_function.py
	This file contains business logic. This file defines the way Alexa responds for certain user input

Place json file in the Alexa Development Console json editor and py file as a AWS lambda function. Map both the files with the help of ADC Endpoint and AWS lambda ARN. Now our Alexa skill is ready to execute. We can test it with the help of ADC test console.

Below are the commands for skill:
1. Smart Shopping: This is entry point for the skill. Alexa will respond nearby stores
2. item list for {store name}
3. what is the price of {itemname}
4. place order for {itemname} for {itemname}
