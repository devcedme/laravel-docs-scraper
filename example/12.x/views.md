# Source: https://laravel.com/docs/12.x/views

# Views

  * Introduction
    * Writing Views in React / Vue
  * Creating and Rendering Views
    * Nested View Directories
    * Creating the First Available View
    * Determining if a View Exists
  * Passing Data to Views
    * Sharing Data With All Views
  * View Composers
    * View Creators
  * Optimizing Views



## Introduction

Of course, it's not practical to return entire HTML documents strings directly from your routes and controllers. Thankfully, views provide a convenient way to place all of our HTML in separate files.

Views separate your controller / application logic from your presentation logic and are stored in the `resources/views` directory. When using Laravel, view templates are usually written using the [Blade templating language](/docs/12.x/blade). A simple view might look something like this:

```blade <!-- View stored in resources/views/greeting.blade.php --> <html> <body> <h1>Hello, {{ $name }}</h1> </body> </html> ``` 

Since this view is stored at `resources/views/greeting.blade.php`, we may return it using the global `view` helper like so:

```php Route::get('/', function () { return view('greeting', ['name' => 'James']); }); ``` 

Looking for more information on how to write Blade templates? Check out the full [Blade documentation](/docs/12.x/blade) to get started.

### Writing Views in React / Vue

Instead of writing their frontend templates in PHP via Blade, many developers have begun to prefer to write their templates using React or Vue. Laravel makes this painless thanks to [Inertia](https://inertiajs.com/), a library that makes it a cinch to tie your React / Vue frontend to your Laravel backend without the typical complexities of building an SPA.

Our [React and Vue application starter kits](/docs/12.x/starter-kits) give you a great starting point for your next Laravel application powered by Inertia.

## Creating and Rendering Views

You may create a view by placing a file with the `.blade.php` extension in your application's `resources/views` directory or by using the `make:view` Artisan command:

```shell php artisan make:view greeting ``` 

The `.blade.php` extension informs the framework that the file contains a [Blade template](/docs/12.x/blade). Blade templates contain HTML as well as Blade directives that allow you to easily echo values, create "if" statements, iterate over data, and more.

Once you have created a view, you may return it from one of your application's routes or controllers using the global `view` helper:

```php Route::get('/', function () { return view('greeting', ['name' => 'James']); }); ``` 

Views may also be returned using the `View` facade:

```php use Illuminate\Support\Facades\View; return View::make('greeting', ['name' => 'James']); ``` 

As you can see, the first argument passed to the `view` helper corresponds to the name of the view file in the `resources/views` directory. The second argument is an array of data that should be made available to the view. In this case, we are passing the `name` variable, which is displayed in the view using [Blade syntax](/docs/12.x/blade).

### Nested View Directories

Views may also be nested within subdirectories of the `resources/views` directory. "Dot" notation may be used to reference nested views. For example, if your view is stored at `resources/views/admin/profile.blade.php`, you may return it from one of your application's routes / controllers like so:

```php return view('admin.profile', $data); ``` 

View directory names should not contain the `.` character.

### Creating the First Available View

Using the `View` facade's `first` method, you may create the first view that exists in a given array of views. This may be useful if your application or package allows views to be customized or overwritten:

```php use Illuminate\Support\Facades\View; return View::first(['custom.admin', 'admin'], $data); ``` 

### Determining if a View Exists

If you need to determine if a view exists, you may use the `View` facade. The `exists` method will return `true` if the view exists:

```php use Illuminate\Support\Facades\View; if (View::exists('admin.profile')) { // ... } ``` 

## Passing Data to Views

As you saw in the previous examples, you may pass an array of data to views to make that data available to the view:

```php return view('greetings', ['name' => 'Victoria']); ``` 

When passing information in this manner, the data should be an array with key / value pairs. After providing data to a view, you can then access each value within your view using the data's keys, such as `<?php echo $name; ?>`.

As an alternative to passing a complete array of data to the `view` helper function, you may use the `with` method to add individual pieces of data to the view. The `with` method returns an instance of the view object so that you can continue chaining methods before returning the view:

```php return view('greeting') ->with('name', 'Victoria') ->with('occupation', 'Astronaut'); ``` 

### Sharing Data With All Views

Occasionally, you may need to share data with all views that are rendered by your application. You may do so using the `View` facade's `share` method. Typically, you should place calls to the `share` method within a service provider's `boot` method. You are free to add them to the `App\Providers\AppServiceProvider` class or generate a separate service provider to house them:

```php <?php namespace App\Providers; use Illuminate\Support\Facades\View; class AppServiceProvider extends ServiceProvider { /** * Register any application services. */ public function register(): void { // ... } /** * Bootstrap any application services. */ public function boot(): void { View::share('key', 'value'); } } ``` 

## View Composers

View composers are callbacks or class methods that are called when a view is rendered. If you have data that you want to be bound to a view each time that view is rendered, a view composer can help you organize that logic into a single location. View composers may prove particularly useful if the same view is returned by multiple routes or controllers within your application and always needs a particular piece of data.

Typically, view composers will be registered within one of your application's [service providers](/docs/12.x/providers). In this example, we'll assume that the `App\Providers\AppServiceProvider` will house this logic.

We'll use the `View` facade's `composer` method to register the view composer. Laravel does not include a default directory for class-based view composers, so you are free to organize them however you wish. For example, you could create an `app/View/Composers` directory to house all of your application's view composers:

```php <?php namespace App\Providers; use App\View\Composers\ProfileComposer; use Illuminate\Support\Facades; use Illuminate\Support\ServiceProvider; use Illuminate\View\View; class AppServiceProvider extends ServiceProvider { /** * Register any application services. */ public function register(): void { // ... } /** * Bootstrap any application services. */ public function boot(): void { // Using class-based composers... Facades\View::composer('profile', ProfileComposer::class); // Using closure-based composers... Facades\View::composer('welcome', function (View $view) { // ... }); Facades\View::composer('dashboard', function (View $view) { // ... }); } } ``` 

Now that we have registered the composer, the `compose` method of the `App\View\Composers\ProfileComposer` class will be executed each time the `profile` view is being rendered. Let's take a look at an example of the composer class:

```php <?php namespace App\View\Composers; use App\Repositories\UserRepository; use Illuminate\View\View; class ProfileComposer { /** * Create a new profile composer. */ public function __construct( protected UserRepository $users, ) {} /** * Bind data to the view. */ public function compose(View $view): void { $view->with('count', $this->users->count()); } } ``` 

As you can see, all view composers are resolved via the [service container](/docs/12.x/container), so you may type-hint any dependencies you need within a composer's constructor.

#### Attaching a Composer to Multiple Views

You may attach a view composer to multiple views at once by passing an array of views as the first argument to the `composer` method:

```php use App\Views\Composers\MultiComposer; use Illuminate\Support\Facades\View; View::composer( ['profile', 'dashboard'], MultiComposer::class ); ``` 

The `composer` method also accepts the `*` character as a wildcard, allowing you to attach a composer to all views:

```php use Illuminate\Support\Facades; use Illuminate\View\View; Facades\View::composer('*', function (View $view) { // ... }); ``` 

### View Creators

View "creators" are very similar to view composers; however, they are executed immediately after the view is instantiated instead of waiting until the view is about to render. To register a view creator, use the `creator` method:

```php use App\View\Creators\ProfileCreator; use Illuminate\Support\Facades\View; View::creator('profile', ProfileCreator::class); ``` 

## Optimizing Views

By default, Blade template views are compiled on demand. When a request is executed that renders a view, Laravel will determine if a compiled version of the view exists. If the file exists, Laravel will then determine if the uncompiled view has been modified more recently than the compiled view. If the compiled view either does not exist, or the uncompiled view has been modified, Laravel will recompile the view.

Compiling views during the request may have a small negative impact on performance, so Laravel provides the `view:cache` Artisan command to precompile all of the views utilized by your application. For increased performance, you may wish to run this command as part of your deployment process:

```shell php artisan view:cache ``` 

You may use the `view:clear` command to clear the view cache:

```shell php artisan view:clear ``` 
