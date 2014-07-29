# PyCSFML - Python bindings for SFML
# Copyright (c) 2014, Oleh Prypin <blaxpirit@gmail.com>
#
# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.


from __future__ import division, absolute_import, print_function

from .ffi import ffi as _ffi
_sf = _ffi.dlopen('libcsfml-network.so')

from . import base
from .util import arg_error as _arg_error


class IpAddress(base.SFMLStruct):
    def __init__(self, address):
        self._sfIpAddress = _ffi.new('sfIpAddress*')
        self.address = address
    
    @property
    def address(self):
        return self._sfIpAddress.address
    @address.setter
    def address(self, value):
        self._sfIpAddress.address = value
    
    def __repr__(self):
        return self._repr('address=')

    @classmethod
    def from_string(cls, address):
        result = _sf.sfIpAddress_fromString(address)
        return cls._wrap_data(result)
    
    @classmethod
    def from_bytes(cls, byte0, byte1, byte2, byte3):
        result = _sf.sfIpAddress_fromBytes(byte0, byte1, byte2, byte3)
        return cls._wrap_data(result)
    
    @classmethod
    def from_integer(cls, address):
        result = _sf.sfIpAddress_fromInteger(address)
        return cls._wrap_data(result)
    
    def to_string(self, string):
        return _sf.sfIpAddress_toString(self._sfIpAddress[0], string)
    
    def to_integer(self):
        return _sf.sfIpAddress_toInteger(self._sfIpAddress[0])
    
    @classmethod
    def get_local_address(cls):
        result = _sf.sfIpAddress_getLocalAddress()
        return cls._wrap_data(result)
    
    @classmethod
    def get_public_address(cls, timeout):
        try: timeout = timeout._sfTime[0]
        except AttributeError: _arg_error('timeout', 'Time')
        result = _sf.sfIpAddress_getPublicAddress(timeout)
        return cls._wrap_data(result)
    

class FtpDirectoryResponse(base.SFMLClass):
    def __del__(self):
        if self._sf_owned: _sf.sfFtpDirectoryResponse_destroy(self._sfFtpDirectoryResponse)
    
    def is_ok(self):
        return _sf.sfFtpDirectoryResponse_isOk(self._sfFtpDirectoryResponse)
    
    def get_status(self):
        return _sf.sfFtpDirectoryResponse_getStatus(self._sfFtpDirectoryResponse)
    
    def get_message(self):
        return _sf.sfFtpDirectoryResponse_getMessage(self._sfFtpDirectoryResponse)
    
    def get_directory(self):
        return _sf.sfFtpDirectoryResponse_getDirectory(self._sfFtpDirectoryResponse)
    

class FtpListingResponse(base.SFMLClass):
    def __del__(self):
        if self._sf_owned: _sf.sfFtpListingResponse_destroy(self._sfFtpListingResponse)
    
    def is_ok(self):
        return _sf.sfFtpListingResponse_isOk(self._sfFtpListingResponse)
    
    def get_status(self):
        return _sf.sfFtpListingResponse_getStatus(self._sfFtpListingResponse)
    
    def get_message(self):
        return _sf.sfFtpListingResponse_getMessage(self._sfFtpListingResponse)
    
    def get_count(self):
        return _sf.sfFtpListingResponse_getCount(self._sfFtpListingResponse)
    
    def get_name(self, index):
        return _sf.sfFtpListingResponse_getName(self._sfFtpListingResponse, index)
    

class FtpResponse(base.SFMLClass):
    def __del__(self):
        if self._sf_owned: _sf.sfFtpResponse_destroy(self._sfFtpResponse)
    
    def is_ok(self):
        return _sf.sfFtpResponse_isOk(self._sfFtpResponse)
    
    def get_status(self):
        return _sf.sfFtpResponse_getStatus(self._sfFtpResponse)
    
    def get_message(self):
        return _sf.sfFtpResponse_getMessage(self._sfFtpResponse)
    

class Ftp(base.SFMLClass):
    def __init__(self, **kwargs):
        self._sfFtp = _sf.sfFtp_create()
        if kwargs: self._set(**kwargs)
    
    def __del__(self):
        if self._sf_owned: _sf.sfFtp_destroy(self._sfFtp)
    
    def connect(self, server, port, timeout):
        try: server = server._sfIpAddress[0]
        except AttributeError: _arg_error('server', 'IpAddress')
        try: timeout = timeout._sfTime[0]
        except AttributeError: _arg_error('timeout', 'Time')
        result = _sf.sfFtp_connect(self._sfFtp, server, port, timeout)
        return FtpResponse._wrap_ptr(result)
    
    def login_anonymous(self):
        result = _sf.sfFtp_loginAnonymous(self._sfFtp)
        return FtpResponse._wrap_ptr(result)
    
    def login(self, user_name, password):
        result = _sf.sfFtp_login(self._sfFtp, user_name, password)
        return FtpResponse._wrap_ptr(result)
    
    def disconnect(self):
        result = _sf.sfFtp_disconnect(self._sfFtp)
        return FtpResponse._wrap_ptr(result)
    
    def keep_alive(self):
        result = _sf.sfFtp_keepAlive(self._sfFtp)
        return FtpResponse._wrap_ptr(result)
    
    def get_working_directory(self):
        result = _sf.sfFtp_getWorkingDirectory(self._sfFtp)
        return FtpDirectoryResponse._wrap_ptr(result)
    
    def get_directory_listing(self, directory):
        result = _sf.sfFtp_getDirectoryListing(self._sfFtp, directory)
        return FtpListingResponse._wrap_ptr(result)
    
    def change_directory(self, directory):
        result = _sf.sfFtp_changeDirectory(self._sfFtp, directory)
        return FtpResponse._wrap_ptr(result)
    
    def parent_directory(self):
        result = _sf.sfFtp_parentDirectory(self._sfFtp)
        return FtpResponse._wrap_ptr(result)
    
    @classmethod
    def directory(cls, ftp, name):
        try: ftp = ftp._sfFtp
        except AttributeError: _arg_error('ftp', 'Ftp')
        result = _sf.sfFtp_createDirectory(ftp, name)
        return FtpResponse._wrap_ptr(result)
    
    def delete_directory(self, name):
        result = _sf.sfFtp_deleteDirectory(self._sfFtp, name)
        return FtpResponse._wrap_ptr(result)
    
    def rename_file(self, file, new_name):
        result = _sf.sfFtp_renameFile(self._sfFtp, file, new_name)
        return FtpResponse._wrap_ptr(result)
    
    def delete_file(self, name):
        result = _sf.sfFtp_deleteFile(self._sfFtp, name)
        return FtpResponse._wrap_ptr(result)
    
    def download(self, distant_file, dest_path, mode):
        result = _sf.sfFtp_download(self._sfFtp, distant_file, dest_path, mode)
        return FtpResponse._wrap_ptr(result)
    
    def upload(self, local_file, dest_path, mode):
        result = _sf.sfFtp_upload(self._sfFtp, local_file, dest_path, mode)
        return FtpResponse._wrap_ptr(result)
    

class HttpRequest(base.SFMLClass):
    def __init__(self, **kwargs):
        self._sfHttpRequest = _sf.sfHttpRequest_create()
        if kwargs: self._set(**kwargs)
    
    def __del__(self):
        if self._sf_owned: _sf.sfHttpRequest_destroy(self._sfHttpRequest)
    
    def set_field(self, field, value):
        return _sf.sfHttpRequest_setField(self._sfHttpRequest, field, value)
    
    def set_method(self, method):
        return _sf.sfHttpRequest_setMethod(self._sfHttpRequest, method)
    
    def set_uri(self, uri):
        return _sf.sfHttpRequest_setUri(self._sfHttpRequest, uri)
    
    def set_http_version(self, major, minor):
        return _sf.sfHttpRequest_setHttpVersion(self._sfHttpRequest, major, minor)
    
    def set_body(self, body):
        return _sf.sfHttpRequest_setBody(self._sfHttpRequest, body)
    

class HttpResponse(base.SFMLClass):
    def __del__(self):
        if self._sf_owned: _sf.sfHttpResponse_destroy(self._sfHttpResponse)
    
    def get_field(self, field):
        return _sf.sfHttpResponse_getField(self._sfHttpResponse, field)
    
    def get_status(self):
        return _sf.sfHttpResponse_getStatus(self._sfHttpResponse)
    
    def get_major_version(self):
        return _sf.sfHttpResponse_getMajorVersion(self._sfHttpResponse)
    
    def get_minor_version(self):
        return _sf.sfHttpResponse_getMinorVersion(self._sfHttpResponse)
    
    def get_body(self):
        return _sf.sfHttpResponse_getBody(self._sfHttpResponse)
    

class Http(base.SFMLClass):
    def __init__(self, **kwargs):
        self._sfHttp = _sf.sfHttp_create()
        if kwargs: self._set(**kwargs)
    
    def __del__(self):
        if self._sf_owned: _sf.sfHttp_destroy(self._sfHttp)
    
    def set_host(self, host, port):
        return _sf.sfHttp_setHost(self._sfHttp, host, port)
    
    def send_request(self, request, timeout):
        try: request = request._sfHttpRequest
        except AttributeError: _arg_error('request', 'HttpRequest')
        try: timeout = timeout._sfTime[0]
        except AttributeError: _arg_error('timeout', 'Time')
        result = _sf.sfHttp_sendRequest(self._sfHttp, request, timeout)
        return HttpResponse._wrap_ptr(result)
    

class Packet(base.SFMLClass):
    def __init__(self, **kwargs):
        self._sfPacket = _sf.sfPacket_create()
        if kwargs: self._set(**kwargs)
    
    def copy(self):
        result = _sf.sfPacket_copy(self._sfPacket)
        return self._wrap_ptr(result)
    
    def __del__(self):
        if self._sf_owned: _sf.sfPacket_destroy(self._sfPacket)
    
    def append(self, data, size_in_bytes):
        return _sf.sfPacket_append(self._sfPacket, data, size_in_bytes)
    
    def clear(self):
        return _sf.sfPacket_clear(self._sfPacket)
    
    def get_data(self):
        return _sf.sfPacket_getData(self._sfPacket)
    
    def get_data_size(self):
        return _sf.sfPacket_getDataSize(self._sfPacket)
    
    def end_of_packet(self):
        return _sf.sfPacket_endOfPacket(self._sfPacket)
    
    def can_read(self):
        return _sf.sfPacket_canRead(self._sfPacket)
    
    def read_bool(self):
        return _sf.sfPacket_readBool(self._sfPacket)
    
    def read_int8(self):
        return _sf.sfPacket_readInt8(self._sfPacket)
    
    def read_uint8(self):
        return _sf.sfPacket_readUint8(self._sfPacket)
    
    def read_int16(self):
        return _sf.sfPacket_readInt16(self._sfPacket)
    
    def read_uint16(self):
        return _sf.sfPacket_readUint16(self._sfPacket)
    
    def read_int32(self):
        return _sf.sfPacket_readInt32(self._sfPacket)
    
    def read_uint32(self):
        return _sf.sfPacket_readUint32(self._sfPacket)
    
    def read_float(self):
        return _sf.sfPacket_readFloat(self._sfPacket)
    
    def read_double(self):
        return _sf.sfPacket_readDouble(self._sfPacket)
    
    def read_string(self, string):
        return _sf.sfPacket_readString(self._sfPacket, string)
    
    def read_wide_string(self, string):
        return _sf.sfPacket_readWideString(self._sfPacket, string)
    
    def write_bool(self, x):
        return _sf.sfPacket_writeBool(self._sfPacket, x)
    
    def write_int8(self, x):
        return _sf.sfPacket_writeInt8(self._sfPacket, x)
    
    def write_uint8(self, x):
        return _sf.sfPacket_writeUint8(self._sfPacket, x)
    
    def write_int16(self, x):
        return _sf.sfPacket_writeInt16(self._sfPacket, x)
    
    def write_uint16(self, x):
        return _sf.sfPacket_writeUint16(self._sfPacket, x)
    
    def write_int32(self, x):
        return _sf.sfPacket_writeInt32(self._sfPacket, x)
    
    def write_uint32(self, x):
        return _sf.sfPacket_writeUint32(self._sfPacket, x)
    
    def write_float(self, x):
        return _sf.sfPacket_writeFloat(self._sfPacket, x)
    
    def write_double(self, x):
        return _sf.sfPacket_writeDouble(self._sfPacket, x)
    
    def write_string(self, string):
        return _sf.sfPacket_writeString(self._sfPacket, string)
    
    def write_wide_string(self, string):
        return _sf.sfPacket_writeWideString(self._sfPacket, string)
    

class SocketSelector(base.SFMLClass):
    def __init__(self, **kwargs):
        self._sfSocketSelector = _sf.sfSocketSelector_create()
        if kwargs: self._set(**kwargs)
    
    def copy(self):
        result = _sf.sfSocketSelector_copy(self._sfSocketSelector)
        return self._wrap_ptr(result)
    
    def __del__(self):
        if self._sf_owned: _sf.sfSocketSelector_destroy(self._sfSocketSelector)
    
    def add_tcp_listener(self, socket):
        try: socket = socket._sfTcpListener
        except AttributeError: _arg_error('socket', 'TcpListener')
        return _sf.sfSocketSelector_addTcpListener(self._sfSocketSelector, socket)
    
    def add_tcp_socket(self, socket):
        try: socket = socket._sfTcpSocket
        except AttributeError: _arg_error('socket', 'TcpSocket')
        return _sf.sfSocketSelector_addTcpSocket(self._sfSocketSelector, socket)
    
    def add_udp_socket(self, socket):
        try: socket = socket._sfUdpSocket
        except AttributeError: _arg_error('socket', 'UdpSocket')
        return _sf.sfSocketSelector_addUdpSocket(self._sfSocketSelector, socket)
    
    def remove_tcp_listener(self, socket):
        try: socket = socket._sfTcpListener
        except AttributeError: _arg_error('socket', 'TcpListener')
        return _sf.sfSocketSelector_removeTcpListener(self._sfSocketSelector, socket)
    
    def remove_tcp_socket(self, socket):
        try: socket = socket._sfTcpSocket
        except AttributeError: _arg_error('socket', 'TcpSocket')
        return _sf.sfSocketSelector_removeTcpSocket(self._sfSocketSelector, socket)
    
    def remove_udp_socket(self, socket):
        try: socket = socket._sfUdpSocket
        except AttributeError: _arg_error('socket', 'UdpSocket')
        return _sf.sfSocketSelector_removeUdpSocket(self._sfSocketSelector, socket)
    
    def clear(self):
        return _sf.sfSocketSelector_clear(self._sfSocketSelector)
    
    def wait(self, timeout):
        try: timeout = timeout._sfTime[0]
        except AttributeError: _arg_error('timeout', 'Time')
        return _sf.sfSocketSelector_wait(self._sfSocketSelector, timeout)
    
    def is_tcp_listener_ready(self, socket):
        try: socket = socket._sfTcpListener
        except AttributeError: _arg_error('socket', 'TcpListener')
        return _sf.sfSocketSelector_isTcpListenerReady(self._sfSocketSelector, socket)
    
    def is_tcp_socket_ready(self, socket):
        try: socket = socket._sfTcpSocket
        except AttributeError: _arg_error('socket', 'TcpSocket')
        return _sf.sfSocketSelector_isTcpSocketReady(self._sfSocketSelector, socket)
    
    def is_udp_socket_ready(self, socket):
        try: socket = socket._sfUdpSocket
        except AttributeError: _arg_error('socket', 'UdpSocket')
        return _sf.sfSocketSelector_isUdpSocketReady(self._sfSocketSelector, socket)
    

class TcpListener(base.SFMLClass):
    def __init__(self, **kwargs):
        self._sfTcpListener = _sf.sfTcpListener_create()
        if kwargs: self._set(**kwargs)
    
    def __del__(self):
        if self._sf_owned: _sf.sfTcpListener_destroy(self._sfTcpListener)
    
    def set_blocking(self, blocking):
        return _sf.sfTcpListener_setBlocking(self._sfTcpListener, blocking)
    
    def is_blocking(self):
        return _sf.sfTcpListener_isBlocking(self._sfTcpListener)
    
    def get_local_port(self):
        return _sf.sfTcpListener_getLocalPort(self._sfTcpListener)
    
    def listen(self, port):
        return _sf.sfTcpListener_listen(self._sfTcpListener, port)
    
    def accept(self, connected):
        try: connected = connected._sfTcpSocket
        except AttributeError: _arg_error('connected', 'TcpSocket')
        return _sf.sfTcpListener_accept(self._sfTcpListener, connected)
    

class TcpSocket(base.SFMLClass):
    def __init__(self, **kwargs):
        self._sfTcpSocket = _sf.sfTcpSocket_create()
        if kwargs: self._set(**kwargs)
    
    def __del__(self):
        if self._sf_owned: _sf.sfTcpSocket_destroy(self._sfTcpSocket)
    
    def set_blocking(self, blocking):
        return _sf.sfTcpSocket_setBlocking(self._sfTcpSocket, blocking)
    
    def is_blocking(self):
        return _sf.sfTcpSocket_isBlocking(self._sfTcpSocket)
    
    def get_local_port(self):
        return _sf.sfTcpSocket_getLocalPort(self._sfTcpSocket)
    
    def get_remote_address(self):
        result = _sf.sfTcpSocket_getRemoteAddress(self._sfTcpSocket)
        return IpAddress._wrap_data(result)
    
    def get_remote_port(self):
        return _sf.sfTcpSocket_getRemotePort(self._sfTcpSocket)
    
    def connect(self, host, port, timeout):
        try: host = host._sfIpAddress[0]
        except AttributeError: _arg_error('host', 'IpAddress')
        try: timeout = timeout._sfTime[0]
        except AttributeError: _arg_error('timeout', 'Time')
        return _sf.sfTcpSocket_connect(self._sfTcpSocket, host, port, timeout)
    
    def disconnect(self):
        return _sf.sfTcpSocket_disconnect(self._sfTcpSocket)
    
    def send(self, data, size):
        return _sf.sfTcpSocket_send(self._sfTcpSocket, data, size)
    
    def receive(self, data, max_size, size_received):
        return _sf.sfTcpSocket_receive(self._sfTcpSocket, data, max_size, size_received)
    
    def send_packet(self, packet):
        try: packet = packet._sfPacket
        except AttributeError: _arg_error('packet', 'Packet')
        return _sf.sfTcpSocket_sendPacket(self._sfTcpSocket, packet)
    
    def receive_packet(self, packet):
        try: packet = packet._sfPacket
        except AttributeError: _arg_error('packet', 'Packet')
        return _sf.sfTcpSocket_receivePacket(self._sfTcpSocket, packet)
    

class UdpSocket(base.SFMLClass):
    def __init__(self, **kwargs):
        self._sfUdpSocket = _sf.sfUdpSocket_create()
        if kwargs: self._set(**kwargs)
    
    def __del__(self):
        if self._sf_owned: _sf.sfUdpSocket_destroy(self._sfUdpSocket)
    
    def set_blocking(self, blocking):
        return _sf.sfUdpSocket_setBlocking(self._sfUdpSocket, blocking)
    
    def is_blocking(self):
        return _sf.sfUdpSocket_isBlocking(self._sfUdpSocket)
    
    def get_local_port(self):
        return _sf.sfUdpSocket_getLocalPort(self._sfUdpSocket)
    
    def bind(self, port):
        return _sf.sfUdpSocket_bind(self._sfUdpSocket, port)
    
    def unbind(self):
        return _sf.sfUdpSocket_unbind(self._sfUdpSocket)
    
    def send(self, data, size, address, port):
        try: address = address._sfIpAddress[0]
        except AttributeError: _arg_error('address', 'IpAddress')
        return _sf.sfUdpSocket_send(self._sfUdpSocket, data, size, address, port)
    
    def receive(self, data, max_size, size_received, address, port):
        try: address = address._sfIpAddress
        except AttributeError: _arg_error('address', 'IpAddress')
        return _sf.sfUdpSocket_receive(self._sfUdpSocket, data, max_size, size_received, address, port)
    
    def send_packet(self, packet, address, port):
        try: packet = packet._sfPacket
        except AttributeError: _arg_error('packet', 'Packet')
        try: address = address._sfIpAddress[0]
        except AttributeError: _arg_error('address', 'IpAddress')
        return _sf.sfUdpSocket_sendPacket(self._sfUdpSocket, packet, address, port)
    
    def receive_packet(self, packet, address, port):
        try: packet = packet._sfPacket
        except AttributeError: _arg_error('packet', 'Packet')
        try: address = address._sfIpAddress
        except AttributeError: _arg_error('address', 'IpAddress')
        return _sf.sfUdpSocket_receivePacket(self._sfUdpSocket, packet, address, port)
    
    @classmethod
    def max_datagram_size(cls):
        return _sf.sfUdpSocket_maxDatagramSize()
    

class FtpTransferMode(base.SFMLEnum):
    BINARY = _sf.sfFtpBinary
    ASCII = _sf.sfFtpAscii
    EBCDIC = _sf.sfFtpEbcdic

class FtpStatus(base.SFMLEnum):
    RESTART_MARKER_REPLY = _sf.sfFtpRestartMarkerReply
    SERVICE_READY_SOON = _sf.sfFtpServiceReadySoon
    DATA_CONNECTION_ALREADY_OPENED = _sf.sfFtpDataConnectionAlreadyOpened
    OPENING_DATA_CONNECTION = _sf.sfFtpOpeningDataConnection
    OK = _sf.sfFtpOk
    POINTLESS_COMMAND = _sf.sfFtpPointlessCommand
    SYSTEM_STATUS = _sf.sfFtpSystemStatus
    DIRECTORY_STATUS = _sf.sfFtpDirectoryStatus
    FILE_STATUS = _sf.sfFtpFileStatus
    HELP_MESSAGE = _sf.sfFtpHelpMessage
    SYSTEM_TYPE = _sf.sfFtpSystemType
    SERVICE_READY = _sf.sfFtpServiceReady
    CLOSING_CONNECTION = _sf.sfFtpClosingConnection
    DATA_CONNECTION_OPENED = _sf.sfFtpDataConnectionOpened
    CLOSING_DATA_CONNECTION = _sf.sfFtpClosingDataConnection
    ENTERING_PASSIVE_MODE = _sf.sfFtpEnteringPassiveMode
    LOGGED_IN = _sf.sfFtpLoggedIn
    FILE_ACTION_OK = _sf.sfFtpFileActionOk
    DIRECTORY_OK = _sf.sfFtpDirectoryOk
    NEED_PASSWORD = _sf.sfFtpNeedPassword
    NEED_ACCOUNT_TO_LOG_IN = _sf.sfFtpNeedAccountToLogIn
    NEED_INFORMATION = _sf.sfFtpNeedInformation
    SERVICE_UNAVAILABLE = _sf.sfFtpServiceUnavailable
    DATA_CONNECTION_UNAVAILABLE = _sf.sfFtpDataConnectionUnavailable
    TRANSFER_ABORTED = _sf.sfFtpTransferAborted
    FILE_ACTION_ABORTED = _sf.sfFtpFileActionAborted
    LOCAL_ERROR = _sf.sfFtpLocalError
    INSUFFICIENT_STORAGE_SPACE = _sf.sfFtpInsufficientStorageSpace
    COMMAND_UNKNOWN = _sf.sfFtpCommandUnknown
    PARAMETERS_UNKNOWN = _sf.sfFtpParametersUnknown
    COMMAND_NOT_IMPLEMENTED = _sf.sfFtpCommandNotImplemented
    BAD_COMMAND_SEQUENCE = _sf.sfFtpBadCommandSequence
    PARAMETER_NOT_IMPLEMENTED = _sf.sfFtpParameterNotImplemented
    NOT_LOGGED_IN = _sf.sfFtpNotLoggedIn
    NEED_ACCOUNT_TO_STORE = _sf.sfFtpNeedAccountToStore
    FILE_UNAVAILABLE = _sf.sfFtpFileUnavailable
    PAGE_TYPE_UNKNOWN = _sf.sfFtpPageTypeUnknown
    NOT_ENOUGH_MEMORY = _sf.sfFtpNotEnoughMemory
    FILENAME_NOT_ALLOWED = _sf.sfFtpFilenameNotAllowed
    INVALID_RESPONSE = _sf.sfFtpInvalidResponse
    CONNECTION_FAILED = _sf.sfFtpConnectionFailed
    CONNECTION_CLOSED = _sf.sfFtpConnectionClosed
    INVALID_FILE = _sf.sfFtpInvalidFile

class HttpMethod(base.SFMLEnum):
    GET = _sf.sfHttpGet
    POST = _sf.sfHttpPost
    HEAD = _sf.sfHttpHead

class HttpStatus(base.SFMLEnum):
    OK = _sf.sfHttpOk
    CREATED = _sf.sfHttpCreated
    ACCEPTED = _sf.sfHttpAccepted
    NO_CONTENT = _sf.sfHttpNoContent
    RESET_CONTENT = _sf.sfHttpResetContent
    PARTIAL_CONTENT = _sf.sfHttpPartialContent
    MULTIPLE_CHOICES = _sf.sfHttpMultipleChoices
    MOVED_PERMANENTLY = _sf.sfHttpMovedPermanently
    MOVED_TEMPORARILY = _sf.sfHttpMovedTemporarily
    NOT_MODIFIED = _sf.sfHttpNotModified
    BAD_REQUEST = _sf.sfHttpBadRequest
    UNAUTHORIZED = _sf.sfHttpUnauthorized
    FORBIDDEN = _sf.sfHttpForbidden
    NOT_FOUND = _sf.sfHttpNotFound
    RANGE_NOT_SATISFIABLE = _sf.sfHttpRangeNotSatisfiable
    INTERNAL_SERVER_ERROR = _sf.sfHttpInternalServerError
    NOT_IMPLEMENTED = _sf.sfHttpNotImplemented
    BAD_GATEWAY = _sf.sfHttpBadGateway
    SERVICE_NOT_AVAILABLE = _sf.sfHttpServiceNotAvailable
    GATEWAY_TIMEOUT = _sf.sfHttpGatewayTimeout
    VERSION_NOT_SUPPORTED = _sf.sfHttpVersionNotSupported
    INVALID_RESPONSE = _sf.sfHttpInvalidResponse
    CONNECTION_FAILED = _sf.sfHttpConnectionFailed

class SocketStatus(base.SFMLEnum):
    DONE = _sf.sfSocketDone
    NOT_READY = _sf.sfSocketNotReady
    DISCONNECTED = _sf.sfSocketDisconnected
    ERROR = _sf.sfSocketError


del base