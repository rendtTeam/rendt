#! /usr/bin/env python3.6
"""
Python 3.6 or newer required.
"""
import json
import os
import stripe
import pprint
# This is your real test secret API key.
stripe.api_key = "sk_test_vc4WnSEYouCgfo0TqHqjUZft00xvqP4xCV"


from flask import Flask, render_template, jsonify, request


app = Flask(__name__, static_folder=".",
            static_url_path="", template_folder=".")


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    """get date time from db calculate total amount of elapsed time"""
    return 10000


@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = request.get_json()
        pprint.pprint(data)
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='usd',
            receipt_email = "fnurlan7@gmail.com",
            # payment_method = 
        )
        print("Output check start----------------------:  ")
        # pprint.pprint(intent)
        # returnedResponse = generate_response(intent)
        # print(type(returnedResponse)
        # print(intent)
        pprint.pprint(generate_response(intent))
        print("Output check finish----------------------:  ")
        return jsonify({
          'clientSecret': intent['client_secret']
        })
    # except Exception as e:
    #     return jsonify(error=str(e)), 404
    except stripe.error.CardError as e:
        print(e.user_message)
        return jsonify({'error': e.user_message})


# @app.route('/create-payment-intent', methods=['POST'])
# def create_payment():
#     data = request.get_json()
#     try:
#         if 'paymentMethodId' in data:
#             order_amount = calculate_order_amount(data['items'])

#             # Create new PaymentIntent with a PaymentMethod ID from the client.
#             intent = stripe.PaymentIntent.create(
#                 amount=order_amount,
#                 currency=data['currency'],
#                 payment_method=data['paymentMethodId'],
#                 confirmation_method='manual',
#                 confirm=True,
#                 # If a mobile client passes `useStripeSdk`, set `use_stripe_sdk=true`
#                 # to take advantage of new authentication features in mobile SDKs.
#                 use_stripe_sdk=True if 'useStripeSdk' in data and data['useStripeSdk'] else None,
#             )
#             # After create, if the PaymentIntent's status is succeeded, fulfill the order.
#         elif 'paymentIntentId' in data:
#             # Confirm the PaymentIntent to finalize payment after handling a required action
#             # on the client.
#             intent = stripe.PaymentIntent.confirm(data['paymentIntentId'])
#             # After confirm, if the PaymentIntent's status is succeeded, fulfill the order.

#         return generate_response(intent)
#     except stripe.error.CardError as e:
#         return jsonify({'error': e.user_message})


def generate_response(intent):
    status = intent['status']
    if status == 'requires_action' or status == 'requires_source_action':
        # Card requires authentication
        print(status)
        return jsonify({'requiresAction': True, 'paymentIntentId': intent['id'], 'clientSecret': intent['client_secret']})
    elif status == 'requires_payment_method' or status == 'requires_source':
        # Card was not properly authenticated, suggest a new payment method
        print(status)
        return jsonify({'error': 'Your card was denied, please provide a new payment method'})
    elif status == 'succeeded':
        # Payment is complete, authentication not required
        # To cancel the payment you will need to issue a Refund (https://stripe.com/docs/api/refunds)
        print("💰 Payment received!")
        return jsonify({'clientSecret': intent['client_secret']})


@app.route('/webhook', methods=['POST'])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    if event_type == 'payment_intent.succeeded':
        print('💰 Payment received!')
        # Fulfill any orders, e-mail receipts, etc
        # To cancel the payment you will need to issue a Refund (https://stripe.com/docs/api/refunds)
    elif event_type == 'payment_intent.payment_failed':
        print('❌ Payment failed.')
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run()