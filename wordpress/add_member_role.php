#!/usr/bin/php7.2
<?php
/*
 * Add role to WP users based on a list of mail adresses.
 *
 * With init snippet fron: https://gist.github.com/hakre/1552239
 * @author Johannes Brakensiek <https://johannes.brakensiek.info>
 * @author dnt
 * @license GPL-3.0+
 */

if(PHP_SAPI !== 'cli')
	exit('CLI only.');

init();
$n = addRoles(stdinStream(), 'mitglied');
echo 'Complete. ' . $n . ' members modified.' . "\n";


function init() : void {
	define('SHORTINIT', true);
	require_once(__DIR__ . '/wp-load.php');
	require_once(ABSPATH . WPINC . '/capabilities.php');
	require_once(ABSPATH . WPINC . '/class-wp-role.php');
	require_once(ABSPATH . WPINC . '/class-wp-roles.php');
	require_once(ABSPATH . WPINC . '/class-wp-session-tokens.php');
	require_once(ABSPATH . WPINC . '/class-wp-user.php');
	require_once(ABSPATH . WPINC . '/class-wp-user-meta-session-tokens.php');
	require_once(ABSPATH . WPINC . '/pluggable.php');
	require_once(ABSPATH . WPINC . '/user.php');
	require_once(ABSPATH . WPINC . '/kses.php');
	require_once(ABSPATH . WPINC . '/rest-api.php');

	wp_plugin_directory_constants();
}

function stdinStream() : \Generator {
    while ($line = fgets(STDIN)) {
        yield trim($line);
    }
}

function addRoles(iterable $membersMail, string $roleName) : int {
	$n = 0;
	foreach($membersMail as $mail) {
		$userdata = WP_User::get_data_by('email', $mail);
		
		if(!$userdata)
			continue;
		
		$user = new WP_User($userdata);
		
		if(empty($user->roles) || !in_array($roleName, $user->roles)) {
			$user->add_role($roleName);
			$n++;
			echo 'Added role ' . $roleName . ' to user using mail address ' . $mail . ".\n";
		}
	}
	
	return $n;
}