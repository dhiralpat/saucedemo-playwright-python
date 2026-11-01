# SauceDemo Playwright Tests (Python)
Automated testing utilizing the Actions table to rerun after a push

## Test Plan
Test-plan table: Test | Steps | Expected result
Standard User Login Test | Login with correct username and password, check you are logged in by webpage and count of items available to purchase on page | Verify login happy path for a user
Login Errors | Run login through a parametrize function where each login is a different state of user login failure | Verify login successfully errors with test provided at each expected_error string variable
Logout Test | Make sure the standard user can login and logout of the webpage. Make sure to check the logged in webpage and sign-in page | Verify happy path for a user to logout of their account after login
Add an item to cart | Add an item to you cart and verify it is in the cart | Verify an items is added to your cart
Remove an item from cart | Add a specific item to your cart and remove it from your cart. Check that no remainders are in the cart | Verify an item is added to your cart and removed
Specific Item added to cart | Add two specific items to your cart and check they are added to your cart page. Use the data-test elements initialized in the conftest.py | Verify the specific item you wanted to add to cart
Remove all items from cart | Add a specific item to your cart and then remove it at the cart page | Verify you removed all items from your cart after adding them


## Tech
Python, pytest, Playwright, GitHub Actions

## How to run
Setup commands: create venv, pip install -r requirements.txt, playwright install chromium, pytest

## Notes
Improving automated testing approaches and seeing where Claude AI can help speed up workflows
