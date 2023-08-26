from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/isPrime/<int:num>')
def checkPrime(num):
    flag = False
    result = {}
    if num == 1:
        print(num, "is not a prime number")
        result = {
            "number": num,
            "isPrime": False,
            "server IP": "122.451.1001.03"

        }
    elif num > 1:
        # check for factors
        for i in range(2, num):
            if (num % i) == 0:
                # if factor is found, set flag to True
                flag = True
                # break out of loop
                break

        if flag:
            result = {
                "number": num,
                "isPrime": False,
                "server IP": "122.451.1001.03"

            }
        else:
            result = {
                "number": num,
                "isPrime": True,
                "server IP": "122.451.1001.03"

            }

    return  jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
