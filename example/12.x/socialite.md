# Source: https://laravel.com/docs/12.x/socialite

# Laravel Socialite

  * Introduction
  * Installation
  * Upgrading Socialite
  * Configuration
  * Authentication
    * Routing
    * Authentication and Storage
    * Access Scopes
    * Slack Bot Scopes
    * Optional Parameters
  * Retrieving User Details



## Introduction

In addition to typical, form based authentication, Laravel also provides a simple, convenient way to authenticate with OAuth providers using [Laravel Socialite](https://github.com/laravel/socialite). Socialite currently supports authentication via Facebook, X, LinkedIn, Google, GitHub, GitLab, Bitbucket, and Slack.

Adapters for other platforms are available via the community driven [Socialite Providers](https://socialiteproviders.com/) website.

## Installation

To get started with Socialite, use the Composer package manager to add the package to your project's dependencies:

```shell composer require laravel/socialite ``` 

## Upgrading Socialite

When upgrading to a new major version of Socialite, it's important that you carefully review [the upgrade guide](https://github.com/laravel/socialite/blob/master/UPGRADE.md).

## Configuration

Before using Socialite, you will need to add credentials for the OAuth providers your application utilizes. Typically, these credentials may be retrieved by creating a "developer application" within the dashboard of the service you will be authenticating with.

These credentials should be placed in your application's `config/services.php` configuration file, and should use the key `facebook`, `x`, `linkedin-openid`, `google`, `github`, `gitlab`, `bitbucket`, `slack`, or `slack-openid`, depending on the providers your application requires:

```php 'github' => [ 'client_id' => env('GITHUB_CLIENT_ID'), 'client_secret' => env('GITHUB_CLIENT_SECRET'), 'redirect' => 'http://example.com/callback-url', ], ``` 

If the `redirect` option contains a relative path, it will automatically be resolved to a fully qualified URL.

## Authentication

### Routing

To authenticate users using an OAuth provider, you will need two routes: one for redirecting the user to the OAuth provider, and another for receiving the callback from the provider after authentication. The example routes below demonstrate the implementation of both routes:

```php use Laravel\Socialite\Facades\Socialite; Route::get('/auth/redirect', function () { return Socialite::driver('github')->redirect(); }); Route::get('/auth/callback', function () { $user = Socialite::driver('github')->user(); // $user->token }); ``` 

The `redirect` method provided by the `Socialite` facade takes care of redirecting the user to the OAuth provider, while the `user` method will examine the incoming request and retrieve the user's information from the provider after they have approved the authentication request.

### Authentication and Storage

Once the user has been retrieved from the OAuth provider, you may determine if the user exists in your application's database and [authenticate the user](/docs/12.x/authentication#authenticate-a-user-instance). If the user does not exist in your application's database, you will typically create a new record in your database to represent the user:

```php use App\Models\User; use Illuminate\Support\Facades\Auth; use Laravel\Socialite\Facades\Socialite; Route::get('/auth/callback', function () { $githubUser = Socialite::driver('github')->user(); $user = User::updateOrCreate([ 'github_id' => $githubUser->id, ], [ 'name' => $githubUser->name, 'email' => $githubUser->email, 'github_token' => $githubUser->token, 'github_refresh_token' => $githubUser->refreshToken, ]); Auth::login($user); return redirect('/dashboard'); }); ``` 

For more information regarding what user information is available from specific OAuth providers, please consult the documentation on retrieving user details.

### Access Scopes

Before redirecting the user, you may use the `scopes` method to specify the "scopes" that should be included in the authentication request. This method will merge all previously specified scopes with the scopes that you specify:

```php use Laravel\Socialite\Facades\Socialite; return Socialite::driver('github') ->scopes(['read:user', 'public_repo']) ->redirect(); ``` 

You can overwrite all existing scopes on the authentication request using the `setScopes` method:

```php return Socialite::driver('github') ->setScopes(['read:user', 'public_repo']) ->redirect(); ``` 

### Slack Bot Scopes

Slack's API provides [different types of access tokens](https://api.slack.com/authentication/token-types), each with their own set of [permission scopes](https://api.slack.com/scopes). Socialite is compatible with both of the following Slack access tokens types:

  * Bot (prefixed with `xoxb-`)
  * User (prefixed with `xoxp-`)



By default, the `slack` driver will generate a `user` token and invoking the driver's `user` method will return the user's details.

Bot tokens are primarily useful if your application will be sending notifications to external Slack workspaces that are owned by your application's users. To generate a bot token, invoke the `asBotUser` method before redirecting the user to Slack for authentication:

```php return Socialite::driver('slack') ->asBotUser() ->setScopes(['chat:write', 'chat:write.public', 'chat:write.customize']) ->redirect(); ``` 

In addition, you must invoke the `asBotUser` method before invoking the `user` method after Slack redirects the user back to your application after authentication:

```php $user = Socialite::driver('slack')->asBotUser()->user(); ``` 

When generating a bot token, the `user` method will still return a `Laravel\Socialite\Two\User` instance; however, only the `token` property will be hydrated. This token may be stored in order to [send notifications to the authenticated user's Slack workspaces](/docs/12.x/notifications#notifying-external-slack-workspaces).

### Optional Parameters

A number of OAuth providers support other optional parameters on the redirect request. To include any optional parameters in the request, call the `with` method with an associative array:

```php use Laravel\Socialite\Facades\Socialite; return Socialite::driver('google') ->with(['hd' => 'example.com']) ->redirect(); ``` 

When using the `with` method, be careful not to pass any reserved keywords such as `state` or `response_type`.

## Retrieving User Details

After the user is redirected back to your application's authentication callback route, you may retrieve the user's details using Socialite's `user` method. The user object returned by the `user` method provides a variety of properties and methods you may use to store information about the user in your own database.

Differing properties and methods may be available on this object depending on whether the OAuth provider you are authenticating with supports OAuth 1.0 or OAuth 2.0:

```php use Laravel\Socialite\Facades\Socialite; Route::get('/auth/callback', function () { $user = Socialite::driver('github')->user(); // OAuth 2.0 providers... $token = $user->token; $refreshToken = $user->refreshToken; $expiresIn = $user->expiresIn; // OAuth 1.0 providers... $token = $user->token; $tokenSecret = $user->tokenSecret; // All providers... $user->getId(); $user->getNickname(); $user->getName(); $user->getEmail(); $user->getAvatar(); }); ``` 

#### Retrieving User Details From a Token

If you already have a valid access token for a user, you can retrieve their user details using Socialite's `userFromToken` method:

```php use Laravel\Socialite\Facades\Socialite; $user = Socialite::driver('github')->userFromToken($token); ``` 

If you are using Facebook Limited Login via an iOS application, Facebook will return an OIDC token instead of an access token. Like an access token, the OIDC token can be provided to the `userFromToken` method in order to retrieve user details.

#### Stateless Authentication

The `stateless` method may be used to disable session state verification. This is useful when adding social authentication to a stateless API that does not utilize cookie based sessions:

```php use Laravel\Socialite\Facades\Socialite; return Socialite::driver('google')->stateless()->user(); ``` 
