# Source: https://laravel.com/docs/12.x/hashing

# Hashing

  * Introduction
  * Configuration
  * Basic Usage
    * Hashing Passwords
    * Verifying That a Password Matches a Hash
    * Determining if a Password Needs to be Rehashed
  * Hash Algorithm Verification



## Introduction

The Laravel `Hash` [facade](/docs/12.x/facades) provides secure Bcrypt and Argon2 hashing for storing user passwords. If you are using one of the [Laravel application starter kits](/docs/12.x/starter-kits), Bcrypt will be used for registration and authentication by default.

Bcrypt is a great choice for hashing passwords because its "work factor" is adjustable, which means that the time it takes to generate a hash can be increased as hardware power increases. When hashing passwords, slow is good. The longer an algorithm takes to hash a password, the longer it takes malicious users to generate "rainbow tables" of all possible string hash values that may be used in brute force attacks against applications.

## Configuration

By default, Laravel uses the `bcrypt` hashing driver when hashing data. However, several other hashing drivers are supported, including [argon](https://en.wikipedia.org/wiki/Argon2) and [argon2id](https://en.wikipedia.org/wiki/Argon2).

You may specify your application's hashing driver using the `HASH_DRIVER` environment variable. But, if you want to customize all of Laravel's hashing driver options, you should publish the complete `hashing` configuration file using the `config:publish` Artisan command:

```shell php artisan config:publish hashing ``` 

## Basic Usage

### Hashing Passwords

You may hash a password by calling the `make` method on the `Hash` facade:

```php <?php namespace App\Http\Controllers; use Illuminate\Http\RedirectResponse; use Illuminate\Http\Request; use Illuminate\Support\Facades\Hash; class PasswordController extends Controller { /** * Update the password for the user. */ public function update(Request $request): RedirectResponse { // Validate the new password length... $request->user()->fill([ 'password' => Hash::make($request->newPassword) ])->save(); return redirect('/profile'); } } ``` 

#### Adjusting The Bcrypt Work Factor

If you are using the Bcrypt algorithm, the `make` method allows you to manage the work factor of the algorithm using the `rounds` option; however, the default work factor managed by Laravel is acceptable for most applications:

```php $hashed = Hash::make('password', [ 'rounds' => 12, ]); ``` 

#### Adjusting The Argon2 Work Factor

If you are using the Argon2 algorithm, the `make` method allows you to manage the work factor of the algorithm using the `memory`, `time`, and `threads` options; however, the default values managed by Laravel are acceptable for most applications:

```php $hashed = Hash::make('password', [ 'memory' => 1024, 'time' => 2, 'threads' => 2, ]); ``` 

For more information on these options, please refer to the [official PHP documentation regarding Argon hashing](https://secure.php.net/manual/en/function.password-hash.php).

### Verifying That a Password Matches a Hash

The `check` method provided by the `Hash` facade allows you to verify that a given plain-text string corresponds to a given hash:

```php if (Hash::check('plain-text', $hashedPassword)) { // The passwords match... } ``` 

### Determining if a Password Needs to be Rehashed

The `needsRehash` method provided by the `Hash` facade allows you to determine if the work factor used by the hasher has changed since the password was hashed. Some applications choose to perform this check during the application's authentication process:

```php if (Hash::needsRehash($hashed)) { $hashed = Hash::make('plain-text'); } ``` 

## Hash Algorithm Verification

To prevent hash algorithm manipulation, Laravel's `Hash::check` method will first verify the given hash was generated using the application's selected hashing algorithm. If the algorithms are different, a `RuntimeException` exception will be thrown.

This is the expected behavior for most applications, where the hashing algorithm is not expected to change and different algorithms can be an indication of a malicious attack. However, if you need to support multiple hashing algorithms within your application, such as when migrating from one algorithm to another, you can disable hash algorithm verification by setting the `HASH_VERIFY` environment variable to `false`:

```ini HASH_VERIFY=false ``` 
