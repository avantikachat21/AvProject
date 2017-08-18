import requests  # allows to send HTTP requests
import urllib  # allows to fetch data across the World Wide Web
import json
import collections
import access_token
import matplotlib.pyplot as plt
import added_sandbox_users

my_token = access_token.token

base_url = "https://api.instagram.com/v1/"  # base url


# --------------------Function to get Self Information--------------------#

def self_info():
    url = base_url + "users/self/?access_token=%s" % (my_token)
    result = requests.get(url).json()
    print(json.dumps(result["data"], indent=3))


# --------------------Function to get information of user from provided username--------------------#

def get_user_info(user_id):
    url = base_url + ("users/%s/?access_token=%s") % (user_id, my_token)
    result = requests.get(url).json()
    print(json.dumps(result["data"], indent=3))


# --------------------Function to get recent media liked by self--------------------#

def recent_media_liked():
    url = base_url + ("users/self/media/liked?access_token=%s") % (my_token)
    result = requests.get(url).json()
    print "The recent media liked by the user is : "
    print (json.dumps(result["data"][0], indent=3))


# --------------------Function to return USER ID--------------------#

def get_user_id(user_name):
    url = (base_url + "users/search?q=%s&access_token=%s") % (user_name, my_token)
    result = requests.get(url).json()
    if result["meta"]["code"] == 200:
        return result["data"][0]["id"]
    else:
        return 0


# --------------------Function to fetch info of self recent post--------------------#

def get_own_post():
    url = base_url + "users/self/media/recent/?access_token=%s" % (my_token)
    result = requests.get(url).json()
    if result["meta"]["code"] == 200:  # checks if the request was sucessfull
        if len(result["data"]):  # check if data is present
            my_posts_info = result["data"][0]
            print(json.dumps(my_posts_info, indent=3))
            return result["data"][0]["id"]
        else:
            print "\nYou have no posts."
    else:
        return 0


# --------------------Function to Check if user exixts and has some Information--------------------#

def search_user(user_name):
    url = (base_url + "users/search?q=%s&access_token=%s") % (user_name, my_token)
    result = requests.get(url).json()
    if result["meta"]["code"] == 200 and len(result["data"]) >= 1:
        print "A User With Such Username Exists."
        return (1)
    else:
        print "Either the Username does not exist in sandbox OR does not contain any information to retrive."
        return (0)


# --------------------Function to get User's post--------------------#

def get_user_post(username):
    user_id = get_user_id(username)
    if user_id == None:
        print "User does'nt exist"
        return None
    else:
        url = base_url + 'users/%s/media/recent/?access_token=%s' % (user_id, my_token)
        user_media = requests.get(url).json()
        if user_media['meta']['code'] == 200:
            if len(user_media['data']):
                # ========MENU TO PUT PARAMETERS FOR SELECTING THE MEDIA========#
                option = int(raw_input(
                    "\nYou want to choose the post on the basis of:\n1. Most Recent\n2. Max Likes\n3. Max Comments\n4. Least Comments.\n5. Least Likes.\nOption: "))

                if option == 1:  # for recent media
                    return user_media['data'][0]['id']

                elif option == 2:  # for media with max likes
                    counter = 1
                    media_id = user_media["data"][0]["id"]
                    max_like = user_media["data"][0]
                    while len(user_media["data"]) > counter:
                        if max_like["likes"]["count"] < user_media["data"][counter]["likes"]["count"]:
                            max_like = user_media["data"][counter]
                            media_id = max_like["id"]
                        counter = counter + 1
                    return media_id

                elif option == 3:  # for media with max comments
                    counter = 1
                    media_id = user_media["data"][0]["id"]
                    max_like = user_media["data"][0]
                    while len(user_media["data"]) > counter:
                        if max_like["comments"]["count"] < user_media["data"][counter]["comments"]["count"]:
                            max_like = user_media["data"][counter]
                            media_id = max_like["id"]
                        counter = counter + 1
                    return media_id

                elif option == 4:  # for media with least comments
                    counter = 1
                    media_id = user_media["data"][0]["id"]
                    max_like = user_media["data"][0]
                    while len(user_media["data"]) > counter:
                        if max_like["comments"]["count"] > user_media["data"][counter]["comments"]["count"]:
                            max_like = user_media["data"][counter]
                            media_id = max_like["id"]
                        counter = counter + 1
                    return media_id

                elif option == 5:  # for media with least likes
                    counter = 1
                    media_id = user_media["data"][0]["id"]
                    max_like = user_media["data"][0]
                    while len(user_media["data"]) > counter:
                        if max_like["likes"]["count"] > user_media["data"][counter]["likes"]["count"]:
                            max_like = user_media["data"][counter]
                            media_id = max_like["id"]
                        counter = counter + 1
                    return media_id

                else:
                    print "\nWrong input....try again.\n"
            else:
                print "\nThere are no posts posted my %s.\n" % (username)
        else:
            print "Status code other than 200 received!"


# --------------------Function to print media comments of a user--------------------#

def view_media_comments(media_id):
    url = base_url + ("media/%s/comments?access_token=%s") % (media_id, my_token)
    result = requests.get(url).json()
    if len(result["data"]) == 0:
        print "\nThere is no comment on this post or the users who have comments are not added to the sandbox.\nMedia id is: %s" % (
        media_id)
    else:
        c = int(raw_input(
            "If you want to see detailed info with comment press 1 else any other number for just comments: \n"))
        if c == 1:
            print (json.dumps(result["data"], indent=3))
        else:
            comments = []
            for i in range(0, len(result["data"])):
                comments.append(result["data"][i]["text"])
            for i in comments:
                print i
        print "\nComments successfully Printed\n"


# --------------------Function to download self recent post--------------------#

def self_download_post():
    url = base_url + "users/self/media/recent/?access_token=%s" % (my_token)
    result = requests.get(url).json()
    image_name = raw_input("Enter the image name you want to save it with (append '.jpeg' at the end): ")
    image_url = result['data'][0]['images']['standard_resolution']['url']
    urllib.urlretrieve(image_url, image_name)
    print "\nYour image has been downloaded successfully!\n"


# --------------------Function to download USER's recent post--------------------#

def user_download_post(user_name, media_id):
    user_id = get_user_id(user_name)
    if user_id != None:
        image_url = ""
        url = (base_url + "users/%s/media/recent/?access_token=%s") % (user_id, my_token)
        user_media = requests.get(url).json()
        image_name = raw_input("\nEnter the image name you want to save it with (append '.jpeg' at the end): ")
        for i in range(0, len(user_media["data"])):
            if user_media["data"][i]["id"] == media_id:
                image_url = user_media['data'][i]['images']['standard_resolution']['url']
                break
        if len(image_url) != 0:
            urllib.urlretrieve(image_url, image_name)
            print "\nYour image has been downloaded successfully!\n"
    else:
        print "User Does not Exist"


# --------------------Function to Comment on a post of user--------------------#

def make_a_comment(user_name):
    media_id = get_user_post(user_name)
    if media_id != None:
        comment = raw_input("Enter the comment you want to post: ")
        payload = {"access_token": my_token, "text": comment}
        request_url = (base_url + "media/%s/comments") % (media_id)
        make_comment = requests.post(request_url, payload).json()
        if make_comment['meta']['code'] == 200:
            print "\nSuccessfully added the comment!\n"
        else:
            print "\nUnable to add the comment. Please try again!"


# --------------------Function to like a post of user--------------------#

def like_a_post(user_name):
    media_id = get_user_post(user_name)
    url = (base_url + 'media/%s/likes') % (media_id)
    payload = {"access_token": my_token}
    post_a_like = requests.post(url, payload).json()
    if post_a_like["meta"]["code"] == 200:
        print "\nThe post has been Liked.\n"
    else:
        print "\nYour like was unsuccessful on the post. Please Try again!\n"


# --------------------Function for Hashtag Analysis of a user--------------------#
def hashtag_analysis(username):
    hashTags = []
    search_url = (base_url + 'users/search?q=%s&access_token=%s') % (username, my_token)
    result = requests.get(search_url).json()
    if result['meta']['code'] == 200:
        if len(result['data']):
            user_id = []
            user_id = (result['data'][0]['id'])
            if user_id == None:
                print "User id does not exist : "
            else:
                url = (base_url + "users/%s/media/recent/?access_token=%s" % (user_id, my_token))
                show_media_details = requests.get(url).json()
                if len(show_media_details['data']):  # loop to get all the hastags of all the media
                    for i in range(0, len(show_media_details["data"])):
                        for j in show_media_details["data"][i]["tags"]:
                            hashTags.append(j)
                    print "All the hashtags that the user has are:\n\n" + str(json.dumps(hashTags, indent=3))

                    # ----------------TO PUT MOST USED HASHTAGS IN ORDER IN LIST AND REMOVING DUPLICATES----------------#
                    counter = {}
                    for i in hashTags: counter[i] = counter.get(i, 0) + 1
                    sorted([(freq, word) for word, freq in counter.items()], reverse=True)
                    max_tags = sorted(counter, key=counter.__getitem__, reverse=True)

                    # ----------------TO PLOT THE HASTAGS ON A PIE-CHART----------------#
                    length = len(max_tags)
                    if length <= 10:
                        print "\nThe hashtags have to be more than 10 in all posts combined to determine interests. Try With differnt user, or add hashtags to your posts.\n"
                    else:
                        last_size = 0
                        for i in range(10, length):
                            last_size += counter[max_tags[i]]
                        labels = "#" + max_tags[0], "#" + max_tags[1], "#" + max_tags[2], "#" + max_tags[3], "#" + \
                                 max_tags[4], "#" + max_tags[5], "#" + max_tags[6], "#" + max_tags[7], "#" + max_tags[
                                     8], "#" + max_tags[9], "others"  # lables to show on the 2 pies
                        sizes = [counter[max_tags[0]], counter[max_tags[1]], counter[max_tags[2]], counter[max_tags[3]],
                                 counter[max_tags[4]], counter[max_tags[5]], counter[max_tags[6]], counter[max_tags[7]],
                                 counter[max_tags[8]], counter[max_tags[9]],
                                 last_size]  # determins the size % of the pie( basically ratios)
                        explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                                   0.1)  # Lifts or explodes the second Pie Outwards 0.2x
                        ffig1, ax1 = plt.subplots()
                        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
                        ax1.axis("EQUAL")  # Equal aspect ratio ensures that pie is drawn as a circle.
                        plt.title("Hashtag Analysis Chart for the user - '%s'." % (username))
                        plt.show()
                else:
                    print "User has no media to operate upon."
        else:
            print "Either the user does not exist or there is no data present to operate on."
    else:
        print "Status code other than 200 recieved."


##################################################################################################################

# ==================================================Main Program==================================================#



print "\n*******WELCOME TO THE INSTA-BOT*******\n"
while True:
    user_option = int(raw_input(
        "Enter the number corresponding to the option you want to perform the actions on:\n1. Self\n2. Other Users\n3. Determine a user's interests based on hashtag analysis of recent posts and plot the same using matplotlib.\n4. Exit.\nOption: "))

    if user_option == 1:
        choice_option = int(raw_input(
            "Do you want to:\n1. Fetch and display your all user details.\n2. Fetch and display your recent post's details.\n3. Recent media liked.\nOption: "))

        # -------------------------MENU FOR SELF USER--------------------------#

        if choice_option == 1:
            self_info()

        elif choice_option == 2:
            my_post_id = get_own_post()

            if my_post_id == 0:
                print "Some other code other than 200 recieved."
            elif my_post_id != None:
                print "\nMy recent post's ID is: " + str(my_post_id)
                print "\nThe recent Image will now be downloaded...."
                self_download_post()

        elif choice_option == 3:
            recent_media_liked()

        else:
            print "\nYou have entered a wrong option. Try again./n"

        continue

    elif user_option == 2:
        print "\nUsers present in the Sandbox are:\n(PLEASE REFER TO TO THE README.md FILE FROM GIT)\n\n(Admin) avantika.i.n.f.i.n.i.t.e"
        for i in added_sandbox_users.added_sandbox_users:
            print i
        username = raw_input("\nEnter the username: ")
        validate_username = search_user(username)

        if validate_username:
            username_choice = int(raw_input(
                "Would you like to:\n1. Get %s 's user ID.\n2. Fetch %s 's POST.\n3. Print general Info of %s.\n4. Get comments on a post of %s.\n5. Make a comment on %s 's post.\n6. Like %s 's post.\nOption: " % (
                username, username, username, username, username, username)))

            # -------------------------MENU FOR OTHER USER--------------------------#

            if username_choice == 1:
                user_id = get_user_id(username)

                if user_id == 0:
                    print "Some Other code than 200 recieved."
                else:
                    print "\nUser ID is: " + str(user_id)

            elif username_choice == 2:
                media_id = get_user_post(username)

                if media_id != None:
                    print "\nThe ID of recent media is: " + str(media_id)
                    print "\nThe Image with above ID will now be downloaded....."
                    user_download_post(username, media_id)

            elif username_choice == 3:
                user_id = get_user_id(username)
                get_user_info(user_id)

            elif username_choice == 4:
                media_id = get_user_post(username)
                if media_id != None:
                    view_media_comments(media_id)

            elif username_choice == 5:
                make_a_comment(username)

            elif username_choice == 6:
                like_a_post(username)

            else:
                print "Wrong input, try again...."
        continue
    elif user_option == 3:
        print "\nUsers present in the Sandbox are:\n(PLEASE REFER TO TO THE README.md FILE FROM GIT)\n\n(Admin) avantika.i.n.f.i.n.i.t.e"
        for i in added_sandbox_users.added_sandbox_users:
            print i
        user_name = raw_input("\nEnter the username: ")
        hashtag_analysis(user_name)
    elif user_option == 4:
        print "\n--------------------------------------------------------------\nThe application will now exit...Thanks for using the INSTA-BOT"
        exit()  # to exit the program
    else:
        print "Wrong Input...Try Again."
    continue