def wPrefersM1OverM(prefer, w, m, m1, N):
    # Check if w prefers m over her current engagement m1
    for i in range(N):
        # If m1 comes before m in list of w,
        # then w prefers her current engagement,
        # don't do anything
        if prefer[w][i] == m1:
            return True

        # If m comes before m1 in w's list,
        # then free her current engagement
        # and engage her with m
        if prefer[w][i] == m:
            return False

def stableMarriage(prefer, N):
    # Stores partner of women. This is our output
    # array that stores passing information.
    # The value of wPartner[i] indicates the partner
    # assigned to woman N+i. Note that the woman numbers
    # between N and 2*N-1. The value -1 indicates
    # that (N+i)'th woman is free
    wPartner = [-1 for _ in range(N)]
    # An array to store availability of men.
    # If mFree[i] is false, then man 'i' is free,
    # otherwise engaged.
    mFree = [False for _ in range(N)]
    freeCount = N

    # While there are free men
    while freeCount > 0:
        # Pick the first free man (we could pick any)
        m = 0
        while m < N:
            if not mFree[m]:
                break
            m += 1

        # One by one go to all women according to
        # m's preferences. Here m is the picked free man
        i = 0
        while i < N and not mFree[m]:
            w = prefer[m][i]

            # The woman of preference is free,
            # w and m become partners (Note that
            # the partnership maybe changed later).
            # So we can say they are engaged not married
            if wPartner[w - N] == -1:
                wPartner[w - N] = m
                mFree[m] = True
                freeCount -= 1
            else:
                # If w is not free
                # Find current engagement of w
                m1 = wPartner[w - N]
                # If w prefers m over her current engagement m1,
                # then break the engagement between w and m1 and
                # engage m with w.
                if not wPrefersM1OverM(prefer, w, m, m1, N):
                    wPartner[w - N] = m
                    mFree[m] = True
                    mFree[m1] = False
            i += 1

    # Print solution
    print("Woman ", " Man")
    for i in range(N):
        print(i + N, "\t", wPartner[i])

# We obtain preference lists from the user for each man or woman to run our algorithm. 
def user_preferences(N):
    prefer = []

    # Input preferences for men
    for i in range(N):
        p_m = input(f"Please enter the preference order of Man {i + 1} (separated with spaces!): ")
        # We split with space to get ['4', '5', '6', '7'] and map to integers to obtain [4, 5, 6, 7]
        listm = list(map(int, p_m.split()))
        # We append lists of men together
        prefer.append(listm)

    # Input preferences for women
    for i in range(N):
        p_w = input(f"Please enter the preference order of Woman {i + 1} (separated with spaces!): ")
        listw = list(map(int, p_w.split()))
        prefer.append(listw)

    stableMarriage(prefer, N)

# We have taken N into the input so we can choose how long we want our lists to be:
N = int(input("Please enter the number of Men or Women taken into Consideration: "))
# We ask for the user's preferences! 
user_preferences(N)
