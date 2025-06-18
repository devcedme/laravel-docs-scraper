# Source: https://laravel.com/docs/12.x/contracts

# Contracts

  * Introduction
    * Contracts vs. Facades
  * When to Use Contracts
  * How to Use Contracts
  * Contract Reference



## Introduction

Laravel's "contracts" are a set of interfaces that define the core services provided by the framework. For example, an `Illuminate\Contracts\Queue\Queue` contract defines the methods needed for queueing jobs, while the `Illuminate\Contracts\Mail\Mailer` contract defines the methods needed for sending e-mail.

Each contract has a corresponding implementation provided by the framework. For example, Laravel provides a queue implementation with a variety of drivers, and a mailer implementation that is powered by [Symfony Mailer](https://symfony.com/doc/current/mailer.html).

All of the Laravel contracts live in [their own GitHub repository](https://github.com/illuminate/contracts). This provides a quick reference point for all available contracts, as well as a single, decoupled package that may be utilized when building packages that interact with Laravel services.

### Contracts vs. Facades

Laravel's [facades](/docs/12.x/facades) and helper functions provide a simple way of utilizing Laravel's services without needing to type-hint and resolve contracts out of the service container. In most cases, each facade has an equivalent contract.

Unlike facades, which do not require you to require them in your class' constructor, contracts allow you to define explicit dependencies for your classes. Some developers prefer to explicitly define their dependencies in this way and therefore prefer to use contracts, while other developers enjoy the convenience of facades. **In general, most applications can use facades without issue during development.**

## When to Use Contracts

The decision to use contracts or facades will come down to personal taste and the tastes of your development team. Both contracts and facades can be used to create robust, well-tested Laravel applications. Contracts and facades are not mutually exclusive. Some parts of your applications may use facades while others depend on contracts. As long as you are keeping your class' responsibilities focused, you will notice very few practical differences between using contracts and facades.

In general, most applications can use facades without issue during development. If you are building a package that integrates with multiple PHP frameworks you may wish to use the `illuminate/contracts` package to define your integration with Laravel's services without the need to require Laravel's concrete implementations in your package's `composer.json` file.

## How to Use Contracts

So, how do you get an implementation of a contract? It's actually quite simple.

Many types of classes in Laravel are resolved through the [service container](/docs/12.x/container), including controllers, event listeners, middleware, queued jobs, and even route closures. So, to get an implementation of a contract, you can just "type-hint" the interface in the constructor of the class being resolved.

For example, take a look at this event listener:

```php <?php namespace App\Listeners; use App\Events\OrderWasPlaced; use App\Models\User; use Illuminate\Contracts\Redis\Factory; class CacheOrderInformation { /** * Create the event listener. */ public function __construct( protected Factory $redis, ) {} /** * Handle the event. */ public function handle(OrderWasPlaced $event): void { // ... } } ``` 

When the event listener is resolved, the service container will read the type-hints on the constructor of the class, and inject the appropriate value. To learn more about registering things in the service container, check out [its documentation](/docs/12.x/container).

## Contract Reference

This table provides a quick reference to all of the Laravel contracts and their equivalent facades:

Contract | References Facade  
---|---  
[Illuminate\Contracts\Auth\Access\Authorizable](https://github.com/illuminate/contracts/blob/12.x/Auth/Access/Authorizable.php) |   
[Illuminate\Contracts\Auth\Access\Gate](https://github.com/illuminate/contracts/blob/12.x/Auth/Access/Gate.php) | `Gate`  
[Illuminate\Contracts\Auth\Authenticatable](https://github.com/illuminate/contracts/blob/12.x/Auth/Authenticatable.php) |   
[Illuminate\Contracts\Auth\CanResetPassword](https://github.com/illuminate/contracts/blob/12.x/Auth/CanResetPassword.php) |   
[Illuminate\Contracts\Auth\Factory](https://github.com/illuminate/contracts/blob/12.x/Auth/Factory.php) | `Auth`  
[Illuminate\Contracts\Auth\Guard](https://github.com/illuminate/contracts/blob/12.x/Auth/Guard.php) | `Auth::guard()`  
[Illuminate\Contracts\Auth\PasswordBroker](https://github.com/illuminate/contracts/blob/12.x/Auth/PasswordBroker.php) | `Password::broker()`  
[Illuminate\Contracts\Auth\PasswordBrokerFactory](https://github.com/illuminate/contracts/blob/12.x/Auth/PasswordBrokerFactory.php) | `Password`  
[Illuminate\Contracts\Auth\StatefulGuard](https://github.com/illuminate/contracts/blob/12.x/Auth/StatefulGuard.php) |   
[Illuminate\Contracts\Auth\SupportsBasicAuth](https://github.com/illuminate/contracts/blob/12.x/Auth/SupportsBasicAuth.php) |   
[Illuminate\Contracts\Auth\UserProvider](https://github.com/illuminate/contracts/blob/12.x/Auth/UserProvider.php) |   
[Illuminate\Contracts\Broadcasting\Broadcaster](https://github.com/illuminate/contracts/blob/12.x/Broadcasting/Broadcaster.php) | `Broadcast::connection()`  
[Illuminate\Contracts\Broadcasting\Factory](https://github.com/illuminate/contracts/blob/12.x/Broadcasting/Factory.php) | `Broadcast`  
[Illuminate\Contracts\Broadcasting\ShouldBroadcast](https://github.com/illuminate/contracts/blob/12.x/Broadcasting/ShouldBroadcast.php) |   
[Illuminate\Contracts\Broadcasting\ShouldBroadcastNow](https://github.com/illuminate/contracts/blob/12.x/Broadcasting/ShouldBroadcastNow.php) |   
[Illuminate\Contracts\Bus\Dispatcher](https://github.com/illuminate/contracts/blob/12.x/Bus/Dispatcher.php) | `Bus`  
[Illuminate\Contracts\Bus\QueueingDispatcher](https://github.com/illuminate/contracts/blob/12.x/Bus/QueueingDispatcher.php) | `Bus::dispatchToQueue()`  
[Illuminate\Contracts\Cache\Factory](https://github.com/illuminate/contracts/blob/12.x/Cache/Factory.php) | `Cache`  
[Illuminate\Contracts\Cache\Lock](https://github.com/illuminate/contracts/blob/12.x/Cache/Lock.php) |   
[Illuminate\Contracts\Cache\LockProvider](https://github.com/illuminate/contracts/blob/12.x/Cache/LockProvider.php) |   
[Illuminate\Contracts\Cache\Repository](https://github.com/illuminate/contracts/blob/12.x/Cache/Repository.php) | `Cache::driver()`  
[Illuminate\Contracts\Cache\Store](https://github.com/illuminate/contracts/blob/12.x/Cache/Store.php) |   
[Illuminate\Contracts\Config\Repository](https://github.com/illuminate/contracts/blob/12.x/Config/Repository.php) | `Config`  
[Illuminate\Contracts\Console\Application](https://github.com/illuminate/contracts/blob/12.x/Console/Application.php) |   
[Illuminate\Contracts\Console\Kernel](https://github.com/illuminate/contracts/blob/12.x/Console/Kernel.php) | `Artisan`  
[Illuminate\Contracts\Container\Container](https://github.com/illuminate/contracts/blob/12.x/Container/Container.php) | `App`  
[Illuminate\Contracts\Cookie\Factory](https://github.com/illuminate/contracts/blob/12.x/Cookie/Factory.php) | `Cookie`  
[Illuminate\Contracts\Cookie\QueueingFactory](https://github.com/illuminate/contracts/blob/12.x/Cookie/QueueingFactory.php) | `Cookie::queue()`  
[Illuminate\Contracts\Database\ModelIdentifier](https://github.com/illuminate/contracts/blob/12.x/Database/ModelIdentifier.php) |   
[Illuminate\Contracts\Debug\ExceptionHandler](https://github.com/illuminate/contracts/blob/12.x/Debug/ExceptionHandler.php) |   
[Illuminate\Contracts\Encryption\Encrypter](https://github.com/illuminate/contracts/blob/12.x/Encryption/Encrypter.php) | `Crypt`  
[Illuminate\Contracts\Events\Dispatcher](https://github.com/illuminate/contracts/blob/12.x/Events/Dispatcher.php) | `Event`  
[Illuminate\Contracts\Filesystem\Cloud](https://github.com/illuminate/contracts/blob/12.x/Filesystem/Cloud.php) | `Storage::cloud()`  
[Illuminate\Contracts\Filesystem\Factory](https://github.com/illuminate/contracts/blob/12.x/Filesystem/Factory.php) | `Storage`  
[Illuminate\Contracts\Filesystem\Filesystem](https://github.com/illuminate/contracts/blob/12.x/Filesystem/Filesystem.php) | `Storage::disk()`  
[Illuminate\Contracts\Foundation\Application](https://github.com/illuminate/contracts/blob/12.x/Foundation/Application.php) | `App`  
[Illuminate\Contracts\Hashing\Hasher](https://github.com/illuminate/contracts/blob/12.x/Hashing/Hasher.php) | `Hash`  
[Illuminate\Contracts\Http\Kernel](https://github.com/illuminate/contracts/blob/12.x/Http/Kernel.php) |   
[Illuminate\Contracts\Mail\Mailable](https://github.com/illuminate/contracts/blob/12.x/Mail/Mailable.php) |   
[Illuminate\Contracts\Mail\Mailer](https://github.com/illuminate/contracts/blob/12.x/Mail/Mailer.php) | `Mail`  
[Illuminate\Contracts\Mail\MailQueue](https://github.com/illuminate/contracts/blob/12.x/Mail/MailQueue.php) | `Mail::queue()`  
[Illuminate\Contracts\Notifications\Dispatcher](https://github.com/illuminate/contracts/blob/12.x/Notifications/Dispatcher.php) | `Notification`  
[Illuminate\Contracts\Notifications\Factory](https://github.com/illuminate/contracts/blob/12.x/Notifications/Factory.php) | `Notification`  
[Illuminate\Contracts\Pagination\LengthAwarePaginator](https://github.com/illuminate/contracts/blob/12.x/Pagination/LengthAwarePaginator.php) |   
[Illuminate\Contracts\Pagination\Paginator](https://github.com/illuminate/contracts/blob/12.x/Pagination/Paginator.php) |   
[Illuminate\Contracts\Pipeline\Hub](https://github.com/illuminate/contracts/blob/12.x/Pipeline/Hub.php) |   
[Illuminate\Contracts\Pipeline\Pipeline](https://github.com/illuminate/contracts/blob/12.x/Pipeline/Pipeline.php) | `Pipeline`  
[Illuminate\Contracts\Queue\EntityResolver](https://github.com/illuminate/contracts/blob/12.x/Queue/EntityResolver.php) |   
[Illuminate\Contracts\Queue\Factory](https://github.com/illuminate/contracts/blob/12.x/Queue/Factory.php) | `Queue`  
[Illuminate\Contracts\Queue\Job](https://github.com/illuminate/contracts/blob/12.x/Queue/Job.php) |   
[Illuminate\Contracts\Queue\Monitor](https://github.com/illuminate/contracts/blob/12.x/Queue/Monitor.php) | `Queue`  
[Illuminate\Contracts\Queue\Queue](https://github.com/illuminate/contracts/blob/12.x/Queue/Queue.php) | `Queue::connection()`  
[Illuminate\Contracts\Queue\QueueableCollection](https://github.com/illuminate/contracts/blob/12.x/Queue/QueueableCollection.php) |   
[Illuminate\Contracts\Queue\QueueableEntity](https://github.com/illuminate/contracts/blob/12.x/Queue/QueueableEntity.php) |   
[Illuminate\Contracts\Queue\ShouldQueue](https://github.com/illuminate/contracts/blob/12.x/Queue/ShouldQueue.php) |   
[Illuminate\Contracts\Redis\Factory](https://github.com/illuminate/contracts/blob/12.x/Redis/Factory.php) | `Redis`  
[Illuminate\Contracts\Routing\BindingRegistrar](https://github.com/illuminate/contracts/blob/12.x/Routing/BindingRegistrar.php) | `Route`  
[Illuminate\Contracts\Routing\Registrar](https://github.com/illuminate/contracts/blob/12.x/Routing/Registrar.php) | `Route`  
[Illuminate\Contracts\Routing\ResponseFactory](https://github.com/illuminate/contracts/blob/12.x/Routing/ResponseFactory.php) | `Response`  
[Illuminate\Contracts\Routing\UrlGenerator](https://github.com/illuminate/contracts/blob/12.x/Routing/UrlGenerator.php) | `URL`  
[Illuminate\Contracts\Routing\UrlRoutable](https://github.com/illuminate/contracts/blob/12.x/Routing/UrlRoutable.php) |   
[Illuminate\Contracts\Session\Session](https://github.com/illuminate/contracts/blob/12.x/Session/Session.php) | `Session::driver()`  
[Illuminate\Contracts\Support\Arrayable](https://github.com/illuminate/contracts/blob/12.x/Support/Arrayable.php) |   
[Illuminate\Contracts\Support\Htmlable](https://github.com/illuminate/contracts/blob/12.x/Support/Htmlable.php) |   
[Illuminate\Contracts\Support\Jsonable](https://github.com/illuminate/contracts/blob/12.x/Support/Jsonable.php) |   
[Illuminate\Contracts\Support\MessageBag](https://github.com/illuminate/contracts/blob/12.x/Support/MessageBag.php) |   
[Illuminate\Contracts\Support\MessageProvider](https://github.com/illuminate/contracts/blob/12.x/Support/MessageProvider.php) |   
[Illuminate\Contracts\Support\Renderable](https://github.com/illuminate/contracts/blob/12.x/Support/Renderable.php) |   
[Illuminate\Contracts\Support\Responsable](https://github.com/illuminate/contracts/blob/12.x/Support/Responsable.php) |   
[Illuminate\Contracts\Translation\Loader](https://github.com/illuminate/contracts/blob/12.x/Translation/Loader.php) |   
[Illuminate\Contracts\Translation\Translator](https://github.com/illuminate/contracts/blob/12.x/Translation/Translator.php) | `Lang`  
[Illuminate\Contracts\Validation\Factory](https://github.com/illuminate/contracts/blob/12.x/Validation/Factory.php) | `Validator`  
[Illuminate\Contracts\Validation\ValidatesWhenResolved](https://github.com/illuminate/contracts/blob/12.x/Validation/ValidatesWhenResolved.php) |   
[Illuminate\Contracts\Validation\ValidationRule](https://github.com/illuminate/contracts/blob/12.x/Validation/ValidationRule.php) |   
[Illuminate\Contracts\Validation\Validator](https://github.com/illuminate/contracts/blob/12.x/Validation/Validator.php) | `Validator::make()`  
[Illuminate\Contracts\View\Engine](https://github.com/illuminate/contracts/blob/12.x/View/Engine.php) |   
[Illuminate\Contracts\View\Factory](https://github.com/illuminate/contracts/blob/12.x/View/Factory.php) | `View`  
[Illuminate\Contracts\View\View](https://github.com/illuminate/contracts/blob/12.x/View/View.php) | `View::make()`
