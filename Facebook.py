import facebook

token = 'EAAENYY1UKrYBAPga8emBOIh8LONvpDwscuhfC7TcMJs42gB0OQFirsz8cyZAOClKbAIYm6QJ6ggcGzMr8bON8SqWQkQHf1qC1Dqs5p5zZBVFZCzPPkfVytpwEzZC4qlfK7Ij0KxG5a9S4G7btocVdfhm1cT5BR5I5ZAHweCe229sanGrBpmRdxQcz7suHO2MZD'
graph = facebook.GraphAPI(access_token=token, version=2.10)

post = graph.get_object(id='445199492349490', edge='members' )
feed = graph.get_connections(id='445199492349490', connection_name='feed')
print (len(feed['data']))