# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class WebSocket(Component):
    """A WebSocket component.
A simple interface to

Keyword arguments:
- state (dict; default {readyState: WebSocket.CONNECTING}): This websocket state (in the readyState prop) and associated information.
- message (dict; optional): When messages are received, this property is updated with the message content.
- error (dict; optional): This property is set with the content of the onerror event.
- send (dict; optional): When this property is set, a message is sent with its content.
- url (string; optional): The websocket endpoint (e.g. wss://echo.websocket.org).
- protocols (list of strings; optional): Supported websocket protocols (optional).
- id (string; optional): The ID used to identify this component in Dash callbacks."""
    @_explicitize_args
    def __init__(self, state=Component.UNDEFINED, message=Component.UNDEFINED, error=Component.UNDEFINED, send=Component.UNDEFINED, url=Component.UNDEFINED, protocols=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['state', 'message', 'error', 'send', 'url', 'protocols', 'id']
        self._type = 'WebSocket'
        self._namespace = 'dash_extensions'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['state', 'message', 'error', 'send', 'url', 'protocols', 'id']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(WebSocket, self).__init__(**args)
