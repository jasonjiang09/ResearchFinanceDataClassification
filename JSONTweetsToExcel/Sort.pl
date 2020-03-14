use strict;
use warnings;
use Path::Class;

use Excel::Writer::XLSX;

my $workbook = Excel::Writer::XLSX->new("Tweet Data.xls");
my $worksheet = $workbook->add_worksheet();

$worksheet->write("A1", "Number of Retweets");
$worksheet->write("B1", "User ID");
$worksheet->write("C1", "URL");
$worksheet->write("D1", "Text");
$worksheet->write("E1", "Username");
$worksheet->write("F1", "Datetime");
$worksheet->write("G1", "is_reply");
$worksheet->write("H1", "is_retweet");
$worksheet->write("I1", "ID");
$worksheet->write("J1", "Number of replies");
$worksheet->write("K1", "Number of favorites");

my $dirname = "/home/jj0523/TweetFiles";
opendir (my $dh, $dirname) || die "Could not open $dirname\n";
my @fileNames = sort { $a cmp $b } readdir($dh);
while (my $file = shift @fileNames) {
    next unless (-f "$dirname/$file");
    next unless ($file =~ m/\.*$/);
    push (@fileNames, $file);
}

my $row = 2;

foreach my $fileName (@fileNames) {
    $fileName = "$dirname/$fileName";
    open my $fh, '<', $fileName or die "Could not open $fileName";
    local $/;
    my $content = <$fh>;
    $content =~ s/"medias": \[.*\], //;
    $content =~ s/"has_media": true, //;

    chop $content for 1;
    $content =~ s/{"usernameTweet": "//;
    
    my @data = split('", "ID": "', $content);
    
    my @temp = split('", "text": "', pop(@data));
    push (@data, @temp);

    @temp = split('", "url": "', pop(@data));
    push (@data, @temp);

    @temp = split('", "nbr_retweet": ', pop(@data));
    push (@data, @temp);

    @temp = split(', "nbr_favorite": ', pop(@data));
    push (@data, @temp);

    @temp = split(', "nbr_reply": ', pop(@data));
    push (@data, @temp);

    @temp = split(', "datetime": "', pop(@data));
    push(@data, @temp);

    @temp = split('", "is_reply": ', pop(@data));
    push(@data, @temp);

    @temp = split(', "is_retweet": ', pop(@data));
    push(@data, @temp);

    @temp = split(', "user_id": "', pop(@data));
    push(@data, @temp);

    #if (index($data[3], "http://") != -1) {
    #    my $temp = substr $data[3], index($data[3], "http://");
    #    $data[3] =~ s/$temp//;
    #}

    #if(index($data[3], "www.") != -1) {
    #    my $temp = substr $data[3], index($data[3], "www.");
    #    $data[3] =~ s/$temp//;
    #}

    my $length = length($data[2]);
    next if($length > 255);
    
    $worksheet->write("A$row", $data[4]);
    $worksheet->write("B$row", $data[10]);
    $worksheet->write("C$row", $data[3]);
    $worksheet->write("D$row", $data[2]);
    $worksheet->write("E$row", $data[0]);
    $worksheet->write("F$row", $data[7]);
    $worksheet->write("G$row", $data[8]);
    $worksheet->write("H$row", $data[9]);
    $worksheet->write("I$row", $data[1]);
    $worksheet->write("J$row", $data[6]);
    $worksheet->write("K$row", $data[5]);
    
    $row += 1;
}



$workbook->close;

closedir($dh);
