<?php 
    $to = "ivan@zdravkov.eu";
    $from = isset($_POST['email']) ? $_POST['email'] : null;
    $name = isset($_POST['name']) ? $_POST['name'] : null;
    $message = isset($_POST['message']) ? $_POST['message'] : null;

    $headersIvan = "From: " . $from . "\r\n" .
        "Reply-To: " . $from . "\r\n" .
        "X-Mailer: PHP/" . phpversion();

    $headersSender = "From: " . $to . "\r\n" .
        "Reply-To: " . $to . "\r\n" .
        "X-Mailer: PHP/" . phpversion();

    $subjectIvan = $name . " sent you a message via your contact form.";
    $subjectSender = "You successfully sent a message to Ivan Zdravkov";
    
    mail($to, $subjectIvan, $message, $headersIvan);
    mail($from, $subjectSender, $message, $headersSender);
?>