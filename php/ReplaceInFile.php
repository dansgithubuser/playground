<?php

function replaceInFile($in, $out, $replacements) {
    $contents = file_get_contents($in);
    //note: the standard doesn't guarantee same order between array_keys and array_values
    //however, it is currently implemented as such
    $contents = str_replace(array_keys($replacements), array_values($replacements), $contents);
    file_put_contents($out, $contents);
}
