package BackupPC::CGI::JSON;

use strict;
use BackupPC::CGI::Lib qw(:all);
use XML::RSS;
use JSON;

sub action
{
    my $protocol = $ENV{HTTPS} eq "on" ?  'https://' : 'http://';
    my $base_url = $protocol . $ENV{'SERVER_NAME'} . $ENV{SCRIPT_NAME};

    my($fullTot, $fullSizeTot, $incrTot, $incrSizeTot, $str,
       $strNone, $strGood, $hostCntGood, $hostCntNone);

    binmode(STDOUT, ":utf8");

    my $rss = new XML::RSS (version => '0.91',
                            encoding => 'utf-8');

    my @json_array;
    my $json = new JSON;

    $rss->channel( title => eval("qq{$Lang->{RSS_Doc_Title}}"),
                   link => $base_url,
                   language => $Conf{Language},
                   description => eval("qq{$Lang->{RSS_Doc_Description}}"),
               );

    $hostCntGood = $hostCntNone = 0;
    GetStatusInfo("hosts");
    my $Privileged = CheckPermission();

    foreach my $host ( GetUserHosts(1) ) {
        my($fullDur, $incrCnt, $incrAge, $fullSize, $fullRate, $reasonHilite);
	my($shortErr);
        my @Backups = $bpc->BackupInfoRead($host);
        my $fullCnt = $incrCnt = 0;
        my $fullAge = $incrAge = -1;

        $bpc->ConfigRead($host);
        %Conf = $bpc->Conf();

        next if ( $Conf{XferMethod} eq "archive" );
        next if ( !$Privileged && !CheckPermission($host) );

        for ( my $i = 0 ; $i < @Backups ; $i++ ) {
            if ( $Backups[$i]{type} eq "full" ) {
                $fullCnt++;
                if ( $fullAge < 0 || $Backups[$i]{startTime} > $fullAge ) {
                    $fullAge  = $Backups[$i]{startTime};
                    $fullSize = $Backups[$i]{size} / (1024 * 1024);
                    $fullDur  = $Backups[$i]{endTime} - $Backups[$i]{startTime};
                }
                $fullSizeTot += $Backups[$i]{size} / (1024 * 1024);
            } else {
                $incrCnt++;
                if ( $incrAge < 0 || $Backups[$i]{startTime} > $incrAge ) {
                    $incrAge = $Backups[$i]{startTime};
                }
                $incrSizeTot += $Backups[$i]{size} / (1024 * 1024);
            }
        }
        if ( $fullAge < 0 ) {
            $fullAge = "";
            $fullRate = "";
        } else {
            $fullAge = sprintf("%.1f", (time - $fullAge) / (24 * 3600));
            $fullRate = sprintf("%.2f",
                                $fullSize / ($fullDur <= 0 ? 1 : $fullDur));
        }
        if ( $incrAge < 0 ) {
            $incrAge = "";
        } else {
            $incrAge = sprintf("%.1f", (time - $incrAge) / (24 * 3600));
        }
        $fullTot += $fullCnt;
        $incrTot += $incrCnt;
        $fullSize = sprintf("%.2f", $fullSize / 1000);
	$incrAge = "&nbsp;" if ( $incrAge eq "" );
	$reasonHilite = $Conf{CgiStatusHilightColor}{$Status{$host}{reason}}
		      || $Conf{CgiStatusHilightColor}{$Status{$host}{state}};
	$reasonHilite = " bgcolor=\"$reasonHilite\"" if ( $reasonHilite ne "" );
        if ( $Status{$host}{state} ne "Status_backup_in_progress"
		&& $Status{$host}{state} ne "Status_restore_in_progress"
		&& $Status{$host}{error} ne "" ) {
	    ($shortErr = $Status{$host}{error}) =~ s/(.{48}).*/$1.../;
	    $shortErr = " ($shortErr)";
	}

        my $host_state = $Lang->{$Status{$host}{state}};
        my $host_last_attempt =  $Lang->{$Status{$host}{reason}} . $shortErr;

        $str = eval("qq{$Lang->{RSS_Host_Summary}}");

        $rss->add_item(title => $host . ', ' . 
                                $host_state . ', ' . 
                                $host_last_attempt,
                       link => $base_url . '?host=' . $host,
                       description => $str);


        push(@json_array, {title => $host . ', ' . 
                                $host_state . ', ' . 
                                $host_last_attempt,
                       link => $base_url . '?host=' . $host,
                       description => $str});
    }

    $fullSizeTot = sprintf("%.2f", $fullSizeTot / 1000);
    $incrSizeTot = sprintf("%.2f", $incrSizeTot / 1000);
    my $now      = timeStamp2(time);

    print 'Content-type: text/json', "\r\n\r\n",
          encode_json(\@json_array);

}

1;
