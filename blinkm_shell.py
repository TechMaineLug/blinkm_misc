#!/usr/bin/perl -w
# 
# A BlinkM shell to use with BlinkMTester Arduino program provided
# here http://thingm.com/fileadmin/thingm/downloads/BlinkM_Examples.zip
# 
# Author: Richard Barnett, Scott Ellis
#

use strict;
use Device::SerialPort;

my $port = Device::SerialPort->new("/dev/ttyUSB0");

$port->baudrate(19200);
$port->parity("none");
$port->handshake("none");
$port->databits(8);
$port->stopbits(1);
$port->read_char_time(0);
$port->read_const_time(20);

# Works without this delay on my workstation.
sleep(1);

$port->write("?");

while (1) {
	my $rx = do_read();

	if ($rx =~ /^\s$/) {
		print "Arduino not responding\n";
	}
	else {
		print "$rx ";
	}

	while (<>) {
		chomp;
		next if /^\s$/;
		exit 0 if /^[Xx]/;
		$port->write($_);
		last;
	}
}

sub do_read
{
	my $response = "";
	my $tries = 50;

	while ($tries-- > 0) {
		my ($count, $data) = $port->read(255);

		if ($count > 0) {
			$response .= $data;
			last if ($data =~ /cmd>/);
		}
	}

	return $response;
}
