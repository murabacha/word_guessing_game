from collections import defaultdict

computer_input = 'ASOOP'
computer_input = computer_input.upper()
attempt = 1

temp_user_input = []
user_inputs = {}
letters = defaultdict(int)
correct_letter = []
for i in computer_input:
    letters[i] += 1
def evaluate(user_input):
    global attempt
    global temp_user_input
    global letters
    global correct_letter
    for i in range(0,5):
        if user_input[i] == computer_input[i]:
            temp_user_input.append([user_input[i],'green'])
            correct_letter.append(i)
            letters[user_input[i]] -= 1

    for i in range(0,5):
        if i in correct_letter:
                continue
        if user_input[i] in computer_input:
            
            if letters[user_input[i]] > 0:
                temp_user_input.insert(i,[user_input[i],'yellow'])
                letters[user_input[i]] -= 1
            elif letters[user_input[i]] <= 0 :
                temp_user_input.insert(i,[user_input[i],'white'])
        else:
            temp_user_input.insert(i,[user_input[i],'white'])
    user_inputs[attempt] = temp_user_input
    temp_user_input = []
    correct_letter = []
    attempt += 1

while attempt < 7:
    user_input = input('enter your 5 letter word\n')
    user_input = user_input.upper()
    evaluate(user_input)

    print(user_inputs)
print(correct_letter)