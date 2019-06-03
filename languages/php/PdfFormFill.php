<?php

function getSimpleObject($contents, $object) {
    $matches = Array();
    preg_match("/{$object} obj[^>]*>>/", $contents, $matches);
    return $matches[0];
}

function getSimpleDictionaryRef($dictionary, $key) {
    $matches = Array();
    preg_match('/\/' . $key . '([^R]+)/', $dictionary, $matches);
    return trim($matches[1]);
}

function getSimpleDictionaryKeys($dictionary) {
    $matches = Array();
    preg_match_all('/\/([^ ]+)/', $dictionary, $matches);
    return $matches[1];
}

/*
This function assumes:
    - PDF file uses Acrobat forms, not XFA forms
    - all field dictionaries are uniquely identified by their partial field name
    - all field dictionaries contain no literal objects
    - all field dictionaries are either off checkboxes or do not have a value set (this is probably many yet-unknown sub-assumptions)
Other than the first item, these seem to be achievable by saving a PDF with Apple's Preview application.
*/
function pdfFormFill($in, $out, $fields) {
    $contents = file_get_contents($in);
    foreach ($fields as $name => $value) {
        //get the object by name
        $pos = strpos($contents, $name);
        $pos_i = strrpos($contents, '<<', $pos - strlen($contents)) + 2;
        $pos_f = strpos($contents, '>>', $pos);
        $object_i = substr($contents, $pos_i, $pos_f - $pos_i);
        //modify the object
        if (is_bool($value)) {
            if (!$value) continue;
            $appearanceDictionaryRef = getSimpleDictionaryRef($object_i, 'AP');
            $appearanceDictionary = getSimpleObject($contents, $appearanceDictionaryRef);
            $normalRef = getSimpleDictionaryRef($appearanceDictionary, 'N');
            $normal = getSimpleObject($contents, $normalRef);
            $keys = getSimpleDictionaryKeys($normal);
            foreach ($keys as $key) if ($key != 'Off') $on = $key;
            $object_f = str_replace('/Off', "/{$on}", $object_i);
        } elseif (is_string($value)) {
            $object_f = $object_i . "/V ({$value})";
        } else {
            throw new Exception("field values must be bools or strings, {$name} is not");
        }
        //replace the object
        $contents = str_replace($object_i, $object_f, $contents);
    }
    file_put_contents($out, $contents);
}
