<?php
/*
$socket = socket_create(AF_INET, SOCK_STREAM, 0);
$result = socket_bind($socket, '0.0.0.0', 5002);
while (true) {
    $result = socket_listen($socket);
    $client =  socket_accept($socket);
    print_r($client);
    echo $input = socket_read($client, 2048);
    $output = 'Input Received: '.$input;
    socket_write($client, $output, strlen($output));پ
    //socket_close($client);
}
socket_close($socket);*/

function unmask($text) {
    $length = ord($text[1]) & 127;
    if($length == 126) {
    $masks = substr($text, 4, 4);
    $data = substr($text, 8);
    }
    elseif($length == 127) {
    $masks = substr($text, 10, 4);
    $data = substr($text, 14);
    }
    else {
    $masks = substr($text, 2, 4);
    $data = substr($text, 6);
    }
    $text = "";
    for ($i = 0; $i < strlen($data); ++$i) {
    $text .= $data[$i] ^ $masks[$i%4];
    }
    return $text;
    }

$address = '0.0.0.0';
$port = 8080;

// Create WebSocket.
$server = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
socket_set_option($server, SOL_SOCKET, SO_REUSEADDR, 1);
socket_bind($server, $address, $port);
socket_listen($server);
$client = socket_accept($server);

// Send WebSocket handshake headers.
$request = socket_read($client, 5000);
preg_match('#Sec-WebSocket-Key: (.*)\r\n#', $request, $matches);
$key = base64_encode(pack(
    'H*',
    sha1($matches[1] . '258EAFA5-E914-47DA-95CA-C5AB0DC85B11')
));

$headers = "HTTP/1.1 101 Switching Protocols\r\n";
$headers .= "Upgrade: websocket\r\n";
$headers .= "Connection: Upgrade\r\n";
$headers .= "Sec-WebSocket-Version: 13\r\n";
$headers .= "Sec-WebSocket-Accept: $key\r\n\r\n";
socket_write($client, $headers, strlen($headers));

// Send messages into WebSocket in a loop.
while (true) {
    sleep(1);
    $input = socket_read($client, 2048);
    echo unmask($input)."\n";
    if (strpos(unmask($input),"lm1"))  
    $content = json_encode(array('Now: '=> time()));
        else
    $content = json_encode(array("msg"=>'prokladě dobrá drezura'));
    //$response = chr(129) . chr(strlen($content)) . $content;
    $response = chr(0x80 | (0x1 & 0x0f)) . chr(strlen($content)) . $content;
     
    
    socket_write($client, $response);
    
    
    
}