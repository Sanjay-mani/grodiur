import razorpay

client = razorpay.Client(auth=("rzp_live_St5ZEParcRHOCW", "nI0ztw6b867PFR0zmYU6be6H"))

try:
    order = client.order.create({
        "amount": 1000,
        "currency": "INR",
        "receipt": "test_receipt",
        "payment_capture": 1
    })
    print("Order created successfully:", order['id'])
except Exception as e:
    print("Error:", str(e))
