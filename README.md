<H1>About</H1>
<p>This library provides the PrimerAPI class to call Primer Delta Flask backend APIs.  The PrimerAPI class creates a REST API session that handles logging, 
  error handling, and automatic retries for all HTTP calls between client and Delta BE.
</p>

<H3>Structure</H3>
<p>
  PrimerAPI &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;root directory </br>
  &nbsp;|</br>
  &nbsp;|--__init__.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;instantiates PrimerAPI class</br>
  &nbsp;|--config.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; used to configure rest session & logging variables.  temp input for JWT</br>
  &nbsp;|--exceptions.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; instantiates error handling classes</br>
  &nbsp;|--rest_session.py&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; instantiates RestSession class.  this class handles all requests library calls for all subordinate functions.</br>
  &nbsp;|--api</br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|</br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|--__init__.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;             does nothing</br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|--searchservice.py &nbsp;&nbsp;&nbsp;&nbsp; instantiates SearchService class.  contains all methods related to search (news / social & summary)</br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|--uploadservice.py &nbsp;&nbsp;&nbsp;&nbsp; instantiates UploadService class.  contains all methods related to data upload</br>
  &nbsp;|--utils</br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|</br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|--__init__.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;          does nothing</br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|--hashing.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; contains function for hashing, this is not implemented but can be used to provide hashIDs for transactions..etc</br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|--munch.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; contains classes / functions for implementing Munch</br>
</p>

<H3>Usage</H3>
1) Import PrimerAPI:
<p>  
  <code>from PrimerAPI import *</code>
</p>

<p> 2) Update config.py file: </p>
<img width="1099" alt="image" src="https://github.com/user-attachments/assets/c477d44a-b097-413c-aecb-60a3a3759ede" />

<p> 3) Instantiate PrimerAPI object: </p>
<code>apiSession = PrimerAPI()
searchTest = apiSession.searchservice.newSearch(filter,queryTerm,queryType,startDate,endDate)
</code>

<H3>To Dos</H3>
<ol>
  <li>Create function to automatically retrieve & refresh JWT</li>
  <li>Add modelservice class / methods to API</li>
  <li>Add additional entity / event extraction classes / methods to API</li>
  <li>Add Muchinfied log examples for improved log search / parsing</li>
</ol>
