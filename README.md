# ANZ-Code
This is a dockerised application which provides RESTFUL APIs to dump customer csv to database, to add a customer, to delete a customer, to create a table, to drop a table. 

## Steps to Run this Repo

1. Take a docker pull
   `docker pull singampallisudheer/anz`
2. Run the image
   ```docker run singampallisudheer/anz```
3. This will start the application on the port `5000`
4. We can hit the APIs as shown below:
5. ```/dump_data/``` --> to dump the data from csv to sqllite
6. GET ```/customer/<cust_no>``` --> to fetch the customer record
7. POST ```/customer ``` --> to add a new customer. Below is the sample input body of POST
 ```json
{
    "cust_no" : 1234,
    "firstname": "firstname",
    "lastname": "lastname",
    "email": "email",
    "city": "city",
    "phonenumber": "042254568"
}
  ```
8. DELETE ```/customer/<cust_no>``` --> to delete a customer
9. ```/drop_table/``` --> to drop a table
