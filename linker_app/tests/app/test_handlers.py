from linker_app.main.service.routes_handlers import handle_link, FetchResponse

#
# def test_handle_link():
#     test_data = {
#         'www.some_url.com': FetchResponse(result=True, errors=False),
#         'wronkg': False}
#
#     for link, res in test_data.items():
#         status = handle_link(link)
#         print(status)
#         assert res == status, status
