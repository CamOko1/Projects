

"""Perform fixed-rate mortgage calculations."""

from argparse import ArgumentParser
import math
import sys


def get_min_payment( principal, annual_interest_rate, term=30, 
                    num_of_payments=12):  
    """
    Initialize a MortgageCalculator object.

        Args:
            principal (float): The total amount of the mortgage
            annual_interest_rate (float): The annual interest rate which is
            expressed as a float between 0 and 1
            years (int): The term of the mortgage in years (default is 30)
            num_of_payments (int): The number of payments per year 
            (default is 12) 
            
        Returns:
            min_payment(int): The minimum mortgage payment that is
            rounded up to the nearest integer
    
        
        """
    P =  principal 
    r = annual_interest_rate / num_of_payments 
    n = term * num_of_payments 
    
    A = P * (r*(1+r)**n) / (((1 + r) ** n) - 1)
    min_payment = math.ceil(A) 
    return min_payment 
def interest_due(balance_of_mortgage, annual_interest_rate,
                num_of_payments = 12): 
    """
    Calculate the amount of interest due in the next mortgage payment.

    Args:
        balance_of_mortgage (float): The balance of the mortgage which is 
        remaining principal
        annual_interest_rate (float): The annual interest rate 
        which is expressed as a float between 0 and 1
        num_of_payments (int): The number of payments per year

    Returns:
        i(float): The amount of interest due in the next payment.
       
        """
    b = balance_of_mortgage 
    r = annual_interest_rate / num_of_payments 
    i = b * r 
    return i 
def remaining_payments(balance_of_mortgage, annual_interest_rate,
                target_payment, num_of_payments = 12): 
    """ 
    Calculate the number of payments required to pay off the mortgage.

    Args:
        balance_of_mortgage (float): The balance of the mortgage which is 
        the remaining principal
        annual_interest_rate (float): The annual interest rate which is
        expressed as a float between 0 and 1
        target_payment (float): The target payment amount
        num_of_payments (int): The number of payments per year

    Returns:
        payments(int): The number of payments required to pay off the mortgage. 
        
        """
    payments = 0
    while balance_of_mortgage > 0:
        interest = interest_due(balance_of_mortgage, annual_interest_rate,
                                num_of_payments)
        principal_payment = target_payment - interest
        balance_of_mortgage -= principal_payment
        payments += 1
    return payments 
def main(principal, annual_interest_rate, years=30, 
         num_of_payments=12, target_payment=None): 
    """  
    Compute and display mortgage-related information.

    Args:
        principal (float): The total amount of the mortgage which is 
        the principal
        annual_interest_rate (float): The annual interest rate which is
        expressed as a float between 0 and 1
        years (int): The term of the mortgage in years (default is 30)
        num_of_payments (int): The number of payments per year 
        (default is 12).
        target_payment (float or None): The user's target payment amount 
        (default is None).

    Side effects:
        Print information to the console
        
        Update the target_payment parameter if it is 
        None and set it to the minimum payment.
        
        Print a message if the target payment is 
        less than the minimum payment.
        
        """
    min_payment = get_min_payment(principal, annual_interest_rate, 
                                  years, num_of_payments)
    print(f"Minimum Payment: ${min_payment}")

    if target_payment is None:
        target_payment = min_payment

    if target_payment < min_payment:
        print("Your target payment is less than the minimum payment for this mortgage.")
    else:
        total_payments = remaining_payments(principal, annual_interest_rate, 
                                            target_payment, num_of_payments)
        print(f"If you make payments of ${target_payment}, you will pay off the mortgage in {total_payments} payments.")

    
    
    





def parse_args(arglist):
    """Parse and validate command-line arguments.
    
    This function expects the following required arguments, in this order:
    
        mortgage_amount (float): total amount of a mortgage
        annual_interest_rate (float): the annual interest rate as a value
            between 0 and 1 (e.g., 0.035 == 3.5%)
        
    This function also allows the following optional arguments:
    
        -y / --years (int): the term of the mortgage in years (default is 30)
        -n / --num_annual_payments (int): the number of annual payments
            (default is 12)
        -p / --target_payment (float): the amount the user wants to pay per
            payment (default is the minimum payment)
    
    Args:
        arglist (list of str): list of command-line arguments.
    
    Returns:
        namespace: the parsed arguments (see argparse documentation for
        more information)
    
    Raises:
        ValueError: encountered an invalid argument.
    """
    # set up argument parser
    parser = ArgumentParser()
    parser.add_argument("mortgage_amount", type=float,
                        help="the total amount of the mortgage")
    parser.add_argument("annual_interest_rate", type=float,
                        help="the annual interest rate, as a float"
                             " between 0 and 1")
    parser.add_argument("-y", "--years", type=int, default=30,
                        help="the term of the mortgage in years (default: 30)")
    parser.add_argument("-n", "--num_annual_payments", type=int, default=12,
                        help="the number of payments per year (default: 12)")
    parser.add_argument("-p", "--target_payment", type=float,
                        help="the amount you want to pay per payment"
                        " (default: the minimum payment)")
    # parse and validate arguments
    args = parser.parse_args()
    if args.mortgage_amount < 0:
        raise ValueError("mortgage amount must be positive")
    if not 0 <= args.annual_interest_rate <= 1:
        raise ValueError("annual interest rate must be between 0 and 1")
    if args.years < 1:
        raise ValueError("years must be positive")
    if args.num_annual_payments < 0:
        raise ValueError("number of payments per year must be positive")
    if args.target_payment and args.target_payment < 0:
        raise ValueError("target payment must be positive")
    
    return args


if __name__ == "__main__":
    try:
        args = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    main(args.mortgage_amount, args.annual_interest_rate, args.years,
         args.num_annual_payments, args.target_payment)

