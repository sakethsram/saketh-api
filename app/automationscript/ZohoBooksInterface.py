import requests
import json


class ZohoBooksInterface:
    _AUTH_URL = "https://accounts.zoho.in/oauth/v2/token"
    _AUTH_GRANT_TYPE = "refresh_token"
    _URL_INVOICE = "https://www.zohoapis.in/books/v3/invoices?organization_id=&ORGID"
    _URL_GET_INVOICE_PDF= "https://www.zohoapis.in/books/v3/invoices/pdf?organization_id=&ORGID&invoice_ids=&INVOICEID"
    _URL_CREATE_EWAYBILL=  "/api/v3/ewaybills"

    def __init__(self, refresh_token,client_id,client_secret,redirect_uri,organization_id):
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.organization_id = organization_id
        self.auth_token = self._generate_token()

    def _generate_token(self):
        api_response = requests.post(
            url=self._AUTH_URL,
            params={
                "refresh_token": self.refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
                "grant_type" : self._AUTH_GRANT_TYPE
            }
        )
        api_response.raise_for_status()
        api_response_json:dict = api_response.json()
        return api_response_json.get("access_token")
    
    def _get_headers(self,content_type="application/json"):
        
        return {
            "Authorization": f"Zoho-oauthtoken {self.auth_token}",
        }
    
    def _get_customer_records(self):

        pass

    def __get_prodcuct_records(self):
        pass

    def create_invoice(self,invoice_detail: dict,should_ignore_auto_number_generation:bool):
        try:
            api_url = self._URL_INVOICE.replace("&ORGID",self.organization_id)
            data_payload = {
                "JSONString" : json.dumps(invoice_detail),
                "ignore_auto_number_generation": should_ignore_auto_number_generation

            }

            api_response = requests.post(
                url=api_url,
                headers=self._get_headers(),
                data=data_payload
            )
            api_response.raise_for_status()
            return "SX",api_response.json()
        except Exception as e:
            print(f"Error in creating an Invoice: Status Code: {api_response.status_code}; Response :{api_response.text} ; Error: {e}")
            return "ERR", e
        
    # def download_invoice_pdf(Self,invoice_id,file_name):
    #     api_url = Self._URL_GET_INVOICE_PDF.replace("&ORGID",Self.organization_id).replace("&INVOICEID",str(invoice_id))
    #     # print(api_url)
    #     api_response = requests.get(api_url,headers=Self._get_headers(),stream=True)
    #     api_response.raise_for_status()

    #     with open(file_name, "wb") as file:
    #         for chunk in api_response.iter_content(chunk_size=8192):  # Adjust chunk size if needed
    #             if chunk:  # Filter out keep-alive chunks
    #                 file.write(chunk)
    
    def download_invoice_pdf(Self,invoice_id):
        try:
            api_url = Self._URL_GET_INVOICE_PDF.replace("&ORGID",Self.organization_id).replace("&INVOICEID",str(invoice_id))
            api_response = requests.get(api_url,headers=Self._get_headers(),stream=True)
            api_response.raise_for_status()
            return "SX", api_response.content
        except Exception as e:
            print(f"Error in downloading an Invoice PDF: Status Code: {api_response.status_code}; Response :{api_response.text} ; Error: {e}")
            return "ERR", e