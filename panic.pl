#!/usr/bin/perl
use strict;
use Device::USB::PanicButton;
use Time::HiRes qw( usleep );
use Cwd qw( abs_path ); 
use FindBin qw($Bin);
use Getopt::Long;

use constant MPLAYER_PATH => '/usr/bin/mplayer';
use constant POLL_INTERVAL => 200000; #nanoseconds

my $nofail = '';
my $verbose = '';
my $help = '';
my $video = $Bin . "/panic-video.avi"; 

GetOptions('nofail' => \$nofail, 'help' => \$help, 'verbose' => \$verbose, 'video=s' => \$video);

if ($help) {
    print(STDERR $0 . " [--nofail] [--verbose] [--video=/path/to/video.avi]
Options:
    --nofail   Persist polling for a panic button, even if none is plugged in
               or if there is an error state.
    --verbose  Print when the button is pushed.
    --video    Specify the video to play instead of the default 'panic-video.avi'.
");
    exit(0);
}

my $pbutton;

if ($verbose) {
    print("Video path is $video \n");
}

while (1) {

    if (!init_pbutton(\$pbutton)) {
	if (!$nofail) {
	    exit(-1);
	}
    } else {
	my $result = $pbutton->pressed();
	if ($result == 1) {
	    if ($verbose) {
		print("ALERT! PANIC!\n");
	    }
	    system(MPLAYER_PATH . " $video -ao sdl &> /dev/null");
	}
    }
    usleep(POLL_INTERVAL);
}

sub init_pbutton {
    my $pbutton = shift(@_);

    if (!$$pbutton) {
	$$pbutton = Device::USB::PanicButton->new();

	if (!$$pbutton) {
	    print(STDERR "Could not create PanicButton USB object.\n");
	    return 0;
	}
    }

    if ($$pbutton->error()) {
	print(STDERR "PanicButton USB object is in error state: " . $$pbutton->error() . "\n");
	undef $$pbutton;
	return 0;
    }
    
    return 1;     
}
