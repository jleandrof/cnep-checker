"""
Module to represent a company database as well as the definitions of various HTTP methods to control it.
"""

from datetime import datetime
from decimal import Decimal
import requests

from flask import make_response, abort


def get_timestamp():
    """ Generates a timestamp

    :return:        formatted date
    """
    return datetime.now().strftime(("%d-%m-%Y %H:%M:%S"))

def get_cnep_status(cnpj):
    """ Get the status of the company in the cnep database

    :return:        goverment information from the cnep database
                    or "Not in cnep database".
    """
    cnepStatus = requests.get('http://www.transparencia.gov.br/api-de-dados/cnep', params={'cnpjSancionado':cnpj}).json()
    if(not cnepStatus):
        cnepStatus = "Not in cnep database"

    return cnepStatus

def format_cnpj(cnpj):
    """ Formats the cnpj number
    :return:        formated string
    """
    cnpj = str(cnpj)
    return "%s.%s.%s/%s-%s" % ( cnpj[0:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:14] )

# Data structure containing the companies to serve with the API
COMPANIES = {
    '00000000000000': {
        'name': 'Test',
        'cnpj': format_cnpj('00000000000000'),
        'cnepStatus': get_cnep_status(00000000000000)
    }
}

def read_all():
    """ Responds with a list of all companies
    
    :return:        List of all the companies
    """
    return COMPANIES

def read_one(cnpj):
    """ Responds with data from one specific company

    :return:        json structure of a company

    """
    return COMPANIES[cnpj]

def get_totals_by_company():
    """
    List the companies along with the total sum of fines each
    of them had to pay.
    :return:        list of companies
    """
    params = {}
    DATA = requests.get('http://www.transparencia.gov.br/api-de-dados/cnep', params=params).json()

    result = {}
    for item in DATA:
        company = item['sancionado']['nome']
        if(company in result.keys()):
            result[company] += Decimal(item['valorMulta'].replace('.', '').replace(',', '.'))
        else:
            result[company] = Decimal(item['valorMulta'].replace('.', '').replace(',', '.'))
    return result

def create(company):
    """
    Creates a new company on database.
    :param company:  company to be created
    :return:        201 on success, 406 if company already exists
    """
    name = company.get("name", None)
    cnpj = company.get("cnpj", None)

    if cnpj not in COMPANIES:
        COMPANIES[cnpj] = {
            "name": name,
            "cnpj": format_cnpj(cnpj),
            "timestamp": get_timestamp(),
            "cnepStatus": get_cnep_status(cnpj)
        }
        return make_response(
            "{name} successfully created".format(name=name), 201
        )
    else:
        abort(
            406,
            "Company already exists"
        )


def update(cnpj, company):
    """
    Update company information on database
    :param cnpj:   cnpj of company to delete
    :param company:  updated information of requested company
    :return:        updated company data
    """
    if cnpj in COMPANIES:
        COMPANIES[cnpj]["name"] = company.get("name", None)
        COMPANIES[cnpj]["timestamp"] = get_timestamp()
        COMPANIES[cnpj]['cnepStatus'] = get_cnep_status(cnpj)

        return COMPANIES[cnpj]
    else:
        abort(
            404, "Company not found"
        )


def delete(cnpj):
    """
    Remove a company from database.
    :param cnpj:   cnpj of company to remove
    :return:        200 on successful delete, 404 if not found
    """
    # Does the person to delete exist?
    if cnpj in COMPANIES:
        companyName = COMPANIES[cnpj]['name']
        del COMPANIES[cnpj]
        return make_response(
            "{companyName} was successfully deleted".format(companyName=companyName), 200
        )
    else:
        abort(
            404, "Company not found"
        )