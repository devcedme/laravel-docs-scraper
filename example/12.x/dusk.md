# Source: https://laravel.com/docs/12.x/dusk

# Laravel Dusk

  * Introduction
  * Installation
    * Managing ChromeDriver Installations
    * Using Other Browsers
  * Getting Started
    * Generating Tests
    * Resetting the Database After Each Test
    * Running Tests
    * Environment Handling
  * Browser Basics
    * Creating Browsers
    * Navigation
    * Resizing Browser Windows
    * Browser Macros
    * Authentication
    * Cookies
    * Executing JavaScript
    * Taking a Screenshot
    * Storing Console Output to Disk
    * Storing Page Source to Disk
  * Interacting With Elements
    * Dusk Selectors
    * Text, Values, and Attributes
    * Interacting With Forms
    * Attaching Files
    * Pressing Buttons
    * Clicking Links
    * Using the Keyboard
    * Using the Mouse
    * JavaScript Dialogs
    * Interacting With Inline Frames
    * Scoping Selectors
    * Waiting for Elements
    * Scrolling an Element Into View
  * Available Assertions
  * Pages
    * Generating Pages
    * Configuring Pages
    * Navigating to Pages
    * Shorthand Selectors
    * Page Methods
  * Components
    * Generating Components
    * Using Components
  * Continuous Integration
    * Heroku CI
    * Travis CI
    * GitHub Actions
    * Chipper CI



## Introduction

[Laravel Dusk](https://github.com/laravel/dusk) provides an expressive, easy-to-use browser automation and testing API. By default, Dusk does not require you to install JDK or Selenium on your local computer. Instead, Dusk uses a standalone [ChromeDriver](https://sites.google.com/chromium.org/driver) installation. However, you are free to utilize any other Selenium compatible driver you wish.

## Installation

To get started, you should install [Google Chrome](https://www.google.com/chrome) and add the `laravel/dusk` Composer dependency to your project:

```shell composer require laravel/dusk --dev ``` 

If you are manually registering Dusk's service provider, you should **never** register it in your production environment, as doing so could lead to arbitrary users being able to authenticate with your application.

After installing the Dusk package, execute the `dusk:install` Artisan command. The `dusk:install` command will create a `tests/Browser` directory, an example Dusk test, and install the Chrome Driver binary for your operating system:

```shell php artisan dusk:install ``` 

Next, set the `APP_URL` environment variable in your application's `.env` file. This value should match the URL you use to access your application in a browser.

If you are using [Laravel Sail](/docs/12.x/sail) to manage your local development environment, please also consult the Sail documentation on [configuring and running Dusk tests](/docs/12.x/sail#laravel-dusk).

### Managing ChromeDriver Installations

If you would like to install a different version of ChromeDriver than what is installed by Laravel Dusk via the `dusk:install` command, you may use the `dusk:chrome-driver` command:

```shell # Install the latest version of ChromeDriver for your OS... php artisan dusk:chrome-driver # Install a given version of ChromeDriver for your OS... php artisan dusk:chrome-driver 86 # Install a given version of ChromeDriver for all supported OSs... php artisan dusk:chrome-driver --all # Install the version of ChromeDriver that matches the detected version of Chrome / Chromium for your OS... php artisan dusk:chrome-driver --detect ``` 

Dusk requires the `chromedriver` binaries to be executable. If you're having problems running Dusk, you should ensure the binaries are executable using the following command: `chmod -R 0755 vendor/laravel/dusk/bin/`.

### Using Other Browsers

By default, Dusk uses Google Chrome and a standalone [ChromeDriver](https://sites.google.com/chromium.org/driver) installation to run your browser tests. However, you may start your own Selenium server and run your tests against any browser you wish.

To get started, open your `tests/DuskTestCase.php` file, which is the base Dusk test case for your application. Within this file, you can remove the call to the `startChromeDriver` method. This will stop Dusk from automatically starting the ChromeDriver:

```php /** * Prepare for Dusk test execution. * * @beforeClass */ public static function prepare(): void { // static::startChromeDriver(); } ``` 

Next, you may modify the `driver` method to connect to the URL and port of your choice. In addition, you may modify the "desired capabilities" that should be passed to the WebDriver:

```php use Facebook\WebDriver\Remote\RemoteWebDriver; /** * Create the RemoteWebDriver instance. */ protected function driver(): RemoteWebDriver { return RemoteWebDriver::create( 'http://localhost:4444/wd/hub', DesiredCapabilities::phantomjs() ); } ``` 

## Getting Started

### Generating Tests

To generate a Dusk test, use the `dusk:make` Artisan command. The generated test will be placed in the `tests/Browser` directory:

```shell php artisan dusk:make LoginTest ``` 

### Resetting the Database After Each Test

Most of the tests you write will interact with pages that retrieve data from your application's database; however, your Dusk tests should never use the `RefreshDatabase` trait. The `RefreshDatabase` trait leverages database transactions which will not be applicable or available across HTTP requests. Instead, you have two options: the `DatabaseMigrations` trait and the `DatabaseTruncation` trait.

#### Using Database Migrations

The `DatabaseMigrations` trait will run your database migrations before each test. However, dropping and re-creating your database tables for each test is typically slower than truncating the tables:

Pest PHPUnit

```php <?php use Illuminate\Foundation\Testing\DatabaseMigrations; use Laravel\Dusk\Browser; uses(DatabaseMigrations::class); // ``` ```php <?php namespace Tests\Browser; use Illuminate\Foundation\Testing\DatabaseMigrations; use Laravel\Dusk\Browser; use Tests\DuskTestCase; class ExampleTest extends DuskTestCase { use DatabaseMigrations; // } ``` 

SQLite in-memory databases may not be used when executing Dusk tests. Since the browser executes within its own process, it will not be able to access the in-memory databases of other processes.

#### Using Database Truncation

The `DatabaseTruncation` trait will migrate your database on the first test in order to ensure your database tables have been properly created. However, on subsequent tests, the database's tables will simply be truncated - providing a speed boost over re-running all of your database migrations:

Pest PHPUnit

```php <?php use Illuminate\Foundation\Testing\DatabaseTruncation; use Laravel\Dusk\Browser; uses(DatabaseTruncation::class); // ``` ```php <?php namespace Tests\Browser; use App\Models\User; use Illuminate\Foundation\Testing\DatabaseTruncation; use Laravel\Dusk\Browser; use Tests\DuskTestCase; class ExampleTest extends DuskTestCase { use DatabaseTruncation; // } ``` 

By default, this trait will truncate all tables except the `migrations` table. If you would like to customize the tables that should be truncated, you may define a `$tablesToTruncate` property on your test class:

If you are using Pest, you should define properties or methods on the base `DuskTestCase` class or on any class your test file extends.

```php /** * Indicates which tables should be truncated. * * @var array */ protected $tablesToTruncate = ['users']; ``` 

Alternatively, you may define an `$exceptTables` property on your test class to specify which tables should be excluded from truncation:

```php /** * Indicates which tables should be excluded from truncation. * * @var array */ protected $exceptTables = ['users']; ``` 

To specify the database connections that should have their tables truncated, you may define a `$connectionsToTruncate` property on your test class:

```php /** * Indicates which connections should have their tables truncated. * * @var array */ protected $connectionsToTruncate = ['mysql']; ``` 

If you would like to execute code before or after database truncation is performed, you may define `beforeTruncatingDatabase` or `afterTruncatingDatabase` methods on your test class:

```php /** * Perform any work that should take place before the database has started truncating. */ protected function beforeTruncatingDatabase(): void { // } /** * Perform any work that should take place after the database has finished truncating. */ protected function afterTruncatingDatabase(): void { // } ``` 

### Running Tests

To run your browser tests, execute the `dusk` Artisan command:

```shell php artisan dusk ``` 

If you had test failures the last time you ran the `dusk` command, you may save time by re-running the failing tests first using the `dusk:fails` command:

```shell php artisan dusk:fails ``` 

The `dusk` command accepts any argument that is normally accepted by the Pest / PHPUnit test runner, such as allowing you to only run the tests for a given [group](https://docs.phpunit.de/en/10.5/annotations.html#group):

```shell php artisan dusk --group=foo ``` 

If you are using [Laravel Sail](/docs/12.x/sail) to manage your local development environment, please consult the Sail documentation on [configuring and running Dusk tests](/docs/12.x/sail#laravel-dusk).

#### Manually Starting ChromeDriver

By default, Dusk will automatically attempt to start ChromeDriver. If this does not work for your particular system, you may manually start ChromeDriver before running the `dusk` command. If you choose to start ChromeDriver manually, you should comment out the following line of your `tests/DuskTestCase.php` file:

```php /** * Prepare for Dusk test execution. * * @beforeClass */ public static function prepare(): void { // static::startChromeDriver(); } ``` 

In addition, if you start ChromeDriver on a port other than 9515, you should modify the `driver` method of the same class to reflect the correct port:

```php use Facebook\WebDriver\Remote\RemoteWebDriver; /** * Create the RemoteWebDriver instance. */ protected function driver(): RemoteWebDriver { return RemoteWebDriver::create( 'http://localhost:9515', DesiredCapabilities::chrome() ); } ``` 

### Environment Handling

To force Dusk to use its own environment file when running tests, create a `.env.dusk.{environment}` file in the root of your project. For example, if you will be initiating the `dusk` command from your `local` environment, you should create a `.env.dusk.local` file.

When running tests, Dusk will back-up your `.env` file and rename your Dusk environment to `.env`. Once the tests have completed, your `.env` file will be restored.

## Browser Basics

### Creating Browsers

To get started, let's write a test that verifies we can log into our application. After generating a test, we can modify it to navigate to the login page, enter some credentials, and click the "Login" button. To create a browser instance, you may call the `browse` method from within your Dusk test:

Pest PHPUnit

```php <?php use App\Models\User; use Illuminate\Foundation\Testing\DatabaseMigrations; use Laravel\Dusk\Browser; uses(DatabaseMigrations::class); test('basic example', function () { $user = User::factory()->create([ 'email' => '[email protected]', ]); $this->browse(function (Browser $browser) use ($user) { $browser->visit('/login') ->type('email', $user->email) ->type('password', 'password') ->press('Login') ->assertPathIs('/home'); }); }); ``` ```php <?php namespace Tests\Browser; use App\Models\User; use Illuminate\Foundation\Testing\DatabaseMigrations; use Laravel\Dusk\Browser; use Tests\DuskTestCase; class ExampleTest extends DuskTestCase { use DatabaseMigrations; /** * A basic browser test example. */ public function test_basic_example(): void { $user = User::factory()->create([ 'email' => '[email protected]', ]); $this->browse(function (Browser $browser) use ($user) { $browser->visit('/login') ->type('email', $user->email) ->type('password', 'password') ->press('Login') ->assertPathIs('/home'); }); } } ``` 

As you can see in the example above, the `browse` method accepts a closure. A browser instance will automatically be passed to this closure by Dusk and is the main object used to interact with and make assertions against your application.

#### Creating Multiple Browsers

Sometimes you may need multiple browsers in order to properly carry out a test. For example, multiple browsers may be needed to test a chat screen that interacts with websockets. To create multiple browsers, simply add more browser arguments to the signature of the closure given to the `browse` method:

```php $this->browse(function (Browser $first, Browser $second) { $first->loginAs(User::find(1)) ->visit('/home') ->waitForText('Message'); $second->loginAs(User::find(2)) ->visit('/home') ->waitForText('Message') ->type('message', 'Hey Taylor') ->press('Send'); $first->waitForText('Hey Taylor') ->assertSee('Jeffrey Way'); }); ``` 

### Navigation

The `visit` method may be used to navigate to a given URI within your application:

```php $browser->visit('/login'); ``` 

You may use the `visitRoute` method to navigate to a [named route](/docs/12.x/routing#named-routes):

```php $browser->visitRoute($routeName, $parameters); ``` 

You may navigate "back" and "forward" using the `back` and `forward` methods:

```php $browser->back(); $browser->forward(); ``` 

You may use the `refresh` method to refresh the page:

```php $browser->refresh(); ``` 

### Resizing Browser Windows

You may use the `resize` method to adjust the size of the browser window:

```php $browser->resize(1920, 1080); ``` 

The `maximize` method may be used to maximize the browser window:

```php $browser->maximize(); ``` 

The `fitContent` method will resize the browser window to match the size of its content:

```php $browser->fitContent(); ``` 

When a test fails, Dusk will automatically resize the browser to fit the content prior to taking a screenshot. You may disable this feature by calling the `disableFitOnFailure` method within your test:

```php $browser->disableFitOnFailure(); ``` 

You may use the `move` method to move the browser window to a different position on your screen:

```php $browser->move($x = 100, $y = 100); ``` 

### Browser Macros

If you would like to define a custom browser method that you can re-use in a variety of your tests, you may use the `macro` method on the `Browser` class. Typically, you should call this method from a [service provider's](/docs/12.x/providers) `boot` method:

```php <?php namespace App\Providers; use Illuminate\Support\ServiceProvider; use Laravel\Dusk\Browser; class DuskServiceProvider extends ServiceProvider { /** * Register Dusk's browser macros. */ public function boot(): void { Browser::macro('scrollToElement', function (string $element = null) { $this->script("$('html, body').animate({ scrollTop: $('$element').offset().top }, 0);"); return $this; }); } } ``` 

The `macro` function accepts a name as its first argument, and a closure as its second. The macro's closure will be executed when calling the macro as a method on a `Browser` instance:

```php $this->browse(function (Browser $browser) use ($user) { $browser->visit('/pay') ->scrollToElement('#credit-card-details') ->assertSee('Enter Credit Card Details'); }); ``` 

### Authentication

Often, you will be testing pages that require authentication. You can use Dusk's `loginAs` method in order to avoid interacting with your application's login screen during every test. The `loginAs` method accepts a primary key associated with your authenticatable model or an authenticatable model instance:

```php use App\Models\User; use Laravel\Dusk\Browser; $this->browse(function (Browser $browser) { $browser->loginAs(User::find(1)) ->visit('/home'); }); ``` 

After using the `loginAs` method, the user session will be maintained for all tests within the file.

### Cookies

You may use the `cookie` method to get or set an encrypted cookie's value. By default, all of the cookies created by Laravel are encrypted:

```php $browser->cookie('name'); $browser->cookie('name', 'Taylor'); ``` 

You may use the `plainCookie` method to get or set an unencrypted cookie's value:

```php $browser->plainCookie('name'); $browser->plainCookie('name', 'Taylor'); ``` 

You may use the `deleteCookie` method to delete the given cookie:

```php $browser->deleteCookie('name'); ``` 

### Executing JavaScript

You may use the `script` method to execute arbitrary JavaScript statements within the browser:

```php $browser->script('document.documentElement.scrollTop = 0'); $browser->script([ 'document.body.scrollTop = 0', 'document.documentElement.scrollTop = 0', ]); $output = $browser->script('return window.location.pathname'); ``` 

### Taking a Screenshot

You may use the `screenshot` method to take a screenshot and store it with the given filename. All screenshots will be stored within the `tests/Browser/screenshots` directory:

```php $browser->screenshot('filename'); ``` 

The `responsiveScreenshots` method may be used to take a series of screenshots at various breakpoints:

```php $browser->responsiveScreenshots('filename'); ``` 

The `screenshotElement` method may be used to take a screenshot of a specific element on the page:

```php $browser->screenshotElement('#selector', 'filename'); ``` 

### Storing Console Output to Disk

You may use the `storeConsoleLog` method to write the current browser's console output to disk with the given filename. Console output will be stored within the `tests/Browser/console` directory:

```php $browser->storeConsoleLog('filename'); ``` 

### Storing Page Source to Disk

You may use the `storeSource` method to write the current page's source to disk with the given filename. The page source will be stored within the `tests/Browser/source` directory:

```php $browser->storeSource('filename'); ``` 

## Interacting With Elements

### Dusk Selectors

Choosing good CSS selectors for interacting with elements is one of the hardest parts of writing Dusk tests. Over time, frontend changes can cause CSS selectors like the following to break your tests:

```html // HTML... <button>Login</button> ``` ```php // Test... $browser->click('.login-page .container div > button'); ``` 

Dusk selectors allow you to focus on writing effective tests rather than remembering CSS selectors. To define a selector, add a `dusk` attribute to your HTML element. Then, when interacting with a Dusk browser, prefix the selector with `@` to manipulate the attached element within your test:

```html // HTML... <button dusk="login-button">Login</button> ``` ```php // Test... $browser->click('@login-button'); ``` 

If desired, you may customize the HTML attribute that the Dusk selector utilizes via the `selectorHtmlAttribute` method. Typically, this method should be called from the `boot` method of your application's `AppServiceProvider`:

```php use Laravel\Dusk\Dusk; Dusk::selectorHtmlAttribute('data-dusk'); ``` 

### Text, Values, and Attributes

#### Retrieving and Setting Values

Dusk provides several methods for interacting with the current value, display text, and attributes of elements on the page. For example, to get the "value" of an element that matches a given CSS or Dusk selector, use the `value` method:

```php // Retrieve the value... $value = $browser->value('selector'); // Set the value... $browser->value('selector', 'value'); ``` 

You may use the `inputValue` method to get the "value" of an input element that has a given field name:

```php $value = $browser->inputValue('field'); ``` 

#### Retrieving Text

The `text` method may be used to retrieve the display text of an element that matches the given selector:

```php $text = $browser->text('selector'); ``` 

#### Retrieving Attributes

Finally, the `attribute` method may be used to retrieve the value of an attribute of an element matching the given selector:

```php $attribute = $browser->attribute('selector', 'value'); ``` 

### Interacting With Forms

#### Typing Values

Dusk provides a variety of methods for interacting with forms and input elements. First, let's take a look at an example of typing text into an input field:

```php $browser->type('email', '[email protected]'); ``` 

Note that, although the method accepts one if necessary, we are not required to pass a CSS selector into the `type` method. If a CSS selector is not provided, Dusk will search for an `input` or `textarea` field with the given `name` attribute.

To append text to a field without clearing its content, you may use the `append` method:

```php $browser->type('tags', 'foo') ->append('tags', ', bar, baz'); ``` 

You may clear the value of an input using the `clear` method:

```php $browser->clear('email'); ``` 

You can instruct Dusk to type slowly using the `typeSlowly` method. By default, Dusk will pause for 100 milliseconds between key presses. To customize the amount of time between key presses, you may pass the appropriate number of milliseconds as the third argument to the method:

```php $browser->typeSlowly('mobile', '+1 (202) 555-5555'); $browser->typeSlowly('mobile', '+1 (202) 555-5555', 300); ``` 

You may use the `appendSlowly` method to append text slowly:

```php $browser->type('tags', 'foo') ->appendSlowly('tags', ', bar, baz'); ``` 

#### Dropdowns

To select a value available on a `select` element, you may use the `select` method. Like the `type` method, the `select` method does not require a full CSS selector. When passing a value to the `select` method, you should pass the underlying option value instead of the display text:

```php $browser->select('size', 'Large'); ``` 

You may select a random option by omitting the second argument:

```php $browser->select('size'); ``` 

By providing an array as the second argument to the `select` method, you can instruct the method to select multiple options:

```php $browser->select('categories', ['Art', 'Music']); ``` 

#### Checkboxes

To "check" a checkbox input, you may use the `check` method. Like many other input related methods, a full CSS selector is not required. If a CSS selector match can't be found, Dusk will search for a checkbox with a matching `name` attribute:

```php $browser->check('terms'); ``` 

The `uncheck` method may be used to "uncheck" a checkbox input:

```php $browser->uncheck('terms'); ``` 

#### Radio Buttons

To "select" a `radio` input option, you may use the `radio` method. Like many other input related methods, a full CSS selector is not required. If a CSS selector match can't be found, Dusk will search for a `radio` input with matching `name` and `value` attributes:

```php $browser->radio('size', 'large'); ``` 

### Attaching Files

The `attach` method may be used to attach a file to a `file` input element. Like many other input related methods, a full CSS selector is not required. If a CSS selector match can't be found, Dusk will search for a `file` input with a matching `name` attribute:

```php $browser->attach('photo', __DIR__.'/photos/mountains.png'); ``` 

The attach function requires the `Zip` PHP extension to be installed and enabled on your server.

### Pressing Buttons

The `press` method may be used to click a button element on the page. The argument given to the `press` method may be either the display text of the button or a CSS / Dusk selector:

```php $browser->press('Login'); ``` 

When submitting forms, many applications disable the form's submission button after it is pressed and then re-enable the button when the form submission's HTTP request is complete. To press a button and wait for the button to be re-enabled, you may use the `pressAndWaitFor` method:

```php // Press the button and wait a maximum of 5 seconds for it to be enabled... $browser->pressAndWaitFor('Save'); // Press the button and wait a maximum of 1 second for it to be enabled... $browser->pressAndWaitFor('Save', 1); ``` 

### Clicking Links

To click a link, you may use the `clickLink` method on the browser instance. The `clickLink` method will click the link that has the given display text:

```php $browser->clickLink($linkText); ``` 

You may use the `seeLink` method to determine if a link with the given display text is visible on the page:

```php if ($browser->seeLink($linkText)) { // ... } ``` 

These methods interact with jQuery. If jQuery is not available on the page, Dusk will automatically inject it into the page so it is available for the test's duration.

### Using the Keyboard

The `keys` method allows you to provide more complex input sequences to a given element than normally allowed by the `type` method. For example, you may instruct Dusk to hold modifier keys while entering values. In this example, the `shift` key will be held while `taylor` is entered into the element matching the given selector. After `taylor` is typed, `swift` will be typed without any modifier keys:

```php $browser->keys('selector', ['{shift}', 'taylor'], 'swift'); ``` 

Another valuable use case for the `keys` method is sending a "keyboard shortcut" combination to the primary CSS selector for your application:

```php $browser->keys('.app', ['{command}', 'j']); ``` 

All modifier keys such as `{command}` are wrapped in `{}` characters, and match the constants defined in the `Facebook\WebDriver\WebDriverKeys` class, which can be [found on GitHub](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php).

#### Fluent Keyboard Interactions

Dusk also provides a `withKeyboard` method, allowing you to fluently perform complex keyboard interactions via the `Laravel\Dusk\Keyboard` class. The `Keyboard` class provides `press`, `release`, `type`, and `pause` methods:

```php use Laravel\Dusk\Keyboard; $browser->withKeyboard(function (Keyboard $keyboard) { $keyboard->press('c') ->pause(1000) ->release('c') ->type(['c', 'e', 'o']); }); ``` 

#### Keyboard Macros

If you would like to define custom keyboard interactions that you can easily re-use throughout your test suite, you may use the `macro` method provided by the `Keyboard` class. Typically, you should call this method from a [service provider's](/docs/12.x/providers) `boot` method:

```php <?php namespace App\Providers; use Facebook\WebDriver\WebDriverKeys; use Illuminate\Support\ServiceProvider; use Laravel\Dusk\Keyboard; use Laravel\Dusk\OperatingSystem; class DuskServiceProvider extends ServiceProvider { /** * Register Dusk's browser macros. */ public function boot(): void { Keyboard::macro('copy', function (string $element = null) { $this->type([ OperatingSystem::onMac() ? WebDriverKeys::META : WebDriverKeys::CONTROL, 'c', ]); return $this; }); Keyboard::macro('paste', function (string $element = null) { $this->type([ OperatingSystem::onMac() ? WebDriverKeys::META : WebDriverKeys::CONTROL, 'v', ]); return $this; }); } } ``` 

The `macro` function accepts a name as its first argument and a closure as its second. The macro's closure will be executed when calling the macro as a method on a `Keyboard` instance:

```php $browser->click('@textarea') ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->copy()) ->click('@another-textarea') ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->paste()); ``` 

### Using the Mouse

#### Clicking on Elements

The `click` method may be used to click on an element matching the given CSS or Dusk selector:

```php $browser->click('.selector'); ``` 

The `clickAtXPath` method may be used to click on an element matching the given XPath expression:

```php $browser->clickAtXPath('//div[@class = "selector"]'); ``` 

The `clickAtPoint` method may be used to click on the topmost element at a given pair of coordinates relative to the viewable area of the browser:

```php $browser->clickAtPoint($x = 0, $y = 0); ``` 

The `doubleClick` method may be used to simulate the double click of a mouse:

```php $browser->doubleClick(); $browser->doubleClick('.selector'); ``` 

The `rightClick` method may be used to simulate the right click of a mouse:

```php $browser->rightClick(); $browser->rightClick('.selector'); ``` 

The `clickAndHold` method may be used to simulate a mouse button being clicked and held down. A subsequent call to the `releaseMouse` method will undo this behavior and release the mouse button:

```php $browser->clickAndHold('.selector'); $browser->clickAndHold() ->pause(1000) ->releaseMouse(); ``` 

The `controlClick` method may be used to simulate the `ctrl+click` event within the browser:

```php $browser->controlClick(); $browser->controlClick('.selector'); ``` 

#### Mouseover

The `mouseover` method may be used when you need to move the mouse over an element matching the given CSS or Dusk selector:

```php $browser->mouseover('.selector'); ``` 

#### Drag and Drop

The `drag` method may be used to drag an element matching the given selector to another element:

```php $browser->drag('.from-selector', '.to-selector'); ``` 

Or, you may drag an element in a single direction:

```php $browser->dragLeft('.selector', $pixels = 10); $browser->dragRight('.selector', $pixels = 10); $browser->dragUp('.selector', $pixels = 10); $browser->dragDown('.selector', $pixels = 10); ``` 

Finally, you may drag an element by a given offset:

```php $browser->dragOffset('.selector', $x = 10, $y = 10); ``` 

### JavaScript Dialogs

Dusk provides various methods to interact with JavaScript Dialogs. For example, you may use the `waitForDialog` method to wait for a JavaScript dialog to appear. This method accepts an optional argument indicating how many seconds to wait for the dialog to appear:

```php $browser->waitForDialog($seconds = null); ``` 

The `assertDialogOpened` method may be used to assert that a dialog has been displayed and contains the given message:

```php $browser->assertDialogOpened('Dialog message'); ``` 

If the JavaScript dialog contains a prompt, you may use the `typeInDialog` method to type a value into the prompt:

```php $browser->typeInDialog('Hello World'); ``` 

To close an open JavaScript dialog by clicking the "OK" button, you may invoke the `acceptDialog` method:

```php $browser->acceptDialog(); ``` 

To close an open JavaScript dialog by clicking the "Cancel" button, you may invoke the `dismissDialog` method:

```php $browser->dismissDialog(); ``` 

### Interacting With Inline Frames

If you need to interact with elements within an iframe, you may use the `withinFrame` method. All element interactions that take place within the closure provided to the `withinFrame` method will be scoped to the context of the specified iframe:

```php $browser->withinFrame('#credit-card-details', function ($browser) { $browser->type('input[name="cardnumber"]', '4242424242424242') ->type('input[name="exp-date"]', '1224') ->type('input[name="cvc"]', '123') ->press('Pay'); }); ``` 

### Scoping Selectors

Sometimes you may wish to perform several operations while scoping all of the operations within a given selector. For example, you may wish to assert that some text exists only within a table and then click a button within that table. You may use the `with` method to accomplish this. All operations performed within the closure given to the `with` method will be scoped to the original selector:

```php $browser->with('.table', function (Browser $table) { $table->assertSee('Hello World') ->clickLink('Delete'); }); ``` 

You may occasionally need to execute assertions outside of the current scope. You may use the `elsewhere` and `elsewhereWhenAvailable` methods to accomplish this:

```php $browser->with('.table', function (Browser $table) { // Current scope is `body .table`... $browser->elsewhere('.page-title', function (Browser $title) { // Current scope is `body .page-title`... $title->assertSee('Hello World'); }); $browser->elsewhereWhenAvailable('.page-title', function (Browser $title) { // Current scope is `body .page-title`... $title->assertSee('Hello World'); }); }); ``` 

### Waiting for Elements

When testing applications that use JavaScript extensively, it often becomes necessary to "wait" for certain elements or data to be available before proceeding with a test. Dusk makes this a cinch. Using a variety of methods, you may wait for elements to become visible on the page or even wait until a given JavaScript expression evaluates to `true`.

#### Waiting

If you just need to pause the test for a given number of milliseconds, use the `pause` method:

```php $browser->pause(1000); ``` 

If you need to pause the test only if a given condition is `true`, use the `pauseIf` method:

```php $browser->pauseIf(App::environment('production'), 1000); ``` 

Likewise, if you need to pause the test unless a given condition is `true`, you may use the `pauseUnless` method:

```php $browser->pauseUnless(App::environment('testing'), 1000); ``` 

#### Waiting for Selectors

The `waitFor` method may be used to pause the execution of the test until the element matching the given CSS or Dusk selector is displayed on the page. By default, this will pause the test for a maximum of five seconds before throwing an exception. If necessary, you may pass a custom timeout threshold as the second argument to the method:

```php // Wait a maximum of five seconds for the selector... $browser->waitFor('.selector'); // Wait a maximum of one second for the selector... $browser->waitFor('.selector', 1); ``` 

You may also wait until the element matching the given selector contains the given text:

```php // Wait a maximum of five seconds for the selector to contain the given text... $browser->waitForTextIn('.selector', 'Hello World'); // Wait a maximum of one second for the selector to contain the given text... $browser->waitForTextIn('.selector', 'Hello World', 1); ``` 

You may also wait until the element matching the given selector is missing from the page:

```php // Wait a maximum of five seconds until the selector is missing... $browser->waitUntilMissing('.selector'); // Wait a maximum of one second until the selector is missing... $browser->waitUntilMissing('.selector', 1); ``` 

Or, you may wait until the element matching the given selector is enabled or disabled:

```php // Wait a maximum of five seconds until the selector is enabled... $browser->waitUntilEnabled('.selector'); // Wait a maximum of one second until the selector is enabled... $browser->waitUntilEnabled('.selector', 1); // Wait a maximum of five seconds until the selector is disabled... $browser->waitUntilDisabled('.selector'); // Wait a maximum of one second until the selector is disabled... $browser->waitUntilDisabled('.selector', 1); ``` 

#### Scoping Selectors When Available

Occasionally, you may wish to wait for an element to appear that matches a given selector and then interact with the element. For example, you may wish to wait until a modal window is available and then press the "OK" button within the modal. The `whenAvailable` method may be used to accomplish this. All element operations performed within the given closure will be scoped to the original selector:

```php $browser->whenAvailable('.modal', function (Browser $modal) { $modal->assertSee('Hello World') ->press('OK'); }); ``` 

#### Waiting for Text

The `waitForText` method may be used to wait until the given text is displayed on the page:

```php // Wait a maximum of five seconds for the text... $browser->waitForText('Hello World'); // Wait a maximum of one second for the text... $browser->waitForText('Hello World', 1); ``` 

You may use the `waitUntilMissingText` method to wait until the displayed text has been removed from the page:

```php // Wait a maximum of five seconds for the text to be removed... $browser->waitUntilMissingText('Hello World'); // Wait a maximum of one second for the text to be removed... $browser->waitUntilMissingText('Hello World', 1); ``` 

#### Waiting for Links

The `waitForLink` method may be used to wait until the given link text is displayed on the page:

```php // Wait a maximum of five seconds for the link... $browser->waitForLink('Create'); // Wait a maximum of one second for the link... $browser->waitForLink('Create', 1); ``` 

#### Waiting for Inputs

The `waitForInput` method may be used to wait until the given input field is visible on the page:

```php // Wait a maximum of five seconds for the input... $browser->waitForInput($field); // Wait a maximum of one second for the input... $browser->waitForInput($field, 1); ``` 

#### Waiting on the Page Location

When making a path assertion such as `$browser->assertPathIs('/home')`, the assertion can fail if `window.location.pathname` is being updated asynchronously. You may use the `waitForLocation` method to wait for the location to be a given value:

```php $browser->waitForLocation('/secret'); ``` 

The `waitForLocation` method can also be used to wait for the current window location to be a fully qualified URL:

```php $browser->waitForLocation('https://example.com/path'); ``` 

You may also wait for a [named route's](/docs/12.x/routing#named-routes) location:

```php $browser->waitForRoute($routeName, $parameters); ``` 

#### Waiting for Page Reloads

If you need to wait for a page to reload after performing an action, use the `waitForReload` method:

```php use Laravel\Dusk\Browser; $browser->waitForReload(function (Browser $browser) { $browser->press('Submit'); }) ->assertSee('Success!'); ``` 

Since the need to wait for the page to reload typically occurs after clicking a button, you may use the `clickAndWaitForReload` method for convenience:

```php $browser->clickAndWaitForReload('.selector') ->assertSee('something'); ``` 

#### Waiting on JavaScript Expressions

Sometimes you may wish to pause the execution of a test until a given JavaScript expression evaluates to `true`. You may easily accomplish this using the `waitUntil` method. When passing an expression to this method, you do not need to include the `return` keyword or an ending semi-colon:

```php // Wait a maximum of five seconds for the expression to be true... $browser->waitUntil('App.data.servers.length > 0'); // Wait a maximum of one second for the expression to be true... $browser->waitUntil('App.data.servers.length > 0', 1); ``` 

#### Waiting on Vue Expressions

The `waitUntilVue` and `waitUntilVueIsNot` methods may be used to wait until a [Vue component](https://vuejs.org) attribute has a given value:

```php // Wait until the component attribute contains the given value... $browser->waitUntilVue('user.name', 'Taylor', '@user'); // Wait until the component attribute doesn't contain the given value... $browser->waitUntilVueIsNot('user.name', null, '@user'); ``` 

#### Waiting for JavaScript Events

The `waitForEvent` method can be used to pause the execution of a test until a JavaScript event occurs:

```php $browser->waitForEvent('load'); ``` 

The event listener is attached to the current scope, which is the `body` element by default. When using a scoped selector, the event listener will be attached to the matching element:

```php $browser->with('iframe', function (Browser $iframe) { // Wait for the iframe's load event... $iframe->waitForEvent('load'); }); ``` 

You may also provide a selector as the second argument to the `waitForEvent` method to attach the event listener to a specific element:

```php $browser->waitForEvent('load', '.selector'); ``` 

You may also wait for events on the `document` and `window` objects:

```php // Wait until the document is scrolled... $browser->waitForEvent('scroll', 'document'); // Wait a maximum of five seconds until the window is resized... $browser->waitForEvent('resize', 'window', 5); ``` 

#### Waiting With a Callback

Many of the "wait" methods in Dusk rely on the underlying `waitUsing` method. You may use this method directly to wait for a given closure to return `true`. The `waitUsing` method accepts the maximum number of seconds to wait, the interval at which the closure should be evaluated, the closure, and an optional failure message:

```php $browser->waitUsing(10, 1, function () use ($something) { return $something->isReady(); }, "Something wasn't ready in time."); ``` 

### Scrolling an Element Into View

Sometimes you may not be able to click on an element because it is outside of the viewable area of the browser. The `scrollIntoView` method will scroll the browser window until the element at the given selector is within the view:

```php $browser->scrollIntoView('.selector') ->click('.selector'); ``` 

## Available Assertions

Dusk provides a variety of assertions that you may make against your application. All of the available assertions are documented in the list below:

assertTitle assertTitleContains assertUrlIs assertSchemeIs assertSchemeIsNot assertHostIs assertHostIsNot assertPortIs assertPortIsNot assertPathBeginsWith assertPathEndsWith assertPathContains assertPathIs assertPathIsNot assertRouteIs assertQueryStringHas assertQueryStringMissing assertFragmentIs assertFragmentBeginsWith assertFragmentIsNot assertHasCookie assertHasPlainCookie assertCookieMissing assertPlainCookieMissing assertCookieValue assertPlainCookieValue assertSee assertDontSee assertSeeIn assertDontSeeIn assertSeeAnythingIn assertSeeNothingIn assertCount assertScript assertSourceHas assertSourceMissing assertSeeLink assertDontSeeLink assertInputValue assertInputValueIsNot assertChecked assertNotChecked assertIndeterminate assertRadioSelected assertRadioNotSelected assertSelected assertNotSelected assertSelectHasOptions assertSelectMissingOptions assertSelectHasOption assertSelectMissingOption assertValue assertValueIsNot assertAttribute assertAttributeMissing assertAttributeContains assertAttributeDoesntContain assertAriaAttribute assertDataAttribute assertVisible assertPresent assertNotPresent assertMissing assertInputPresent assertInputMissing assertDialogOpened assertEnabled assertDisabled assertButtonEnabled assertButtonDisabled assertFocused assertNotFocused assertAuthenticated assertGuest assertAuthenticatedAs assertVue assertVueIsNot assertVueContains assertVueDoesntContain

#### assertTitle

Assert that the page title matches the given text:

```php $browser->assertTitle($title); ``` 

#### assertTitleContains

Assert that the page title contains the given text:

```php $browser->assertTitleContains($title); ``` 

#### assertUrlIs

Assert that the current URL (without the query string) matches the given string:

```php $browser->assertUrlIs($url); ``` 

#### assertSchemeIs

Assert that the current URL scheme matches the given scheme:

```php $browser->assertSchemeIs($scheme); ``` 

#### assertSchemeIsNot

Assert that the current URL scheme does not match the given scheme:

```php $browser->assertSchemeIsNot($scheme); ``` 

#### assertHostIs

Assert that the current URL host matches the given host:

```php $browser->assertHostIs($host); ``` 

#### assertHostIsNot

Assert that the current URL host does not match the given host:

```php $browser->assertHostIsNot($host); ``` 

#### assertPortIs

Assert that the current URL port matches the given port:

```php $browser->assertPortIs($port); ``` 

#### assertPortIsNot

Assert that the current URL port does not match the given port:

```php $browser->assertPortIsNot($port); ``` 

#### assertPathBeginsWith

Assert that the current URL path begins with the given path:

```php $browser->assertPathBeginsWith('/home'); ``` 

#### assertPathEndsWith

Assert that the current URL path ends with the given path:

```php $browser->assertPathEndsWith('/home'); ``` 

#### assertPathContains

Assert that the current URL path contains the given path:

```php $browser->assertPathContains('/home'); ``` 

#### assertPathIs

Assert that the current path matches the given path:

```php $browser->assertPathIs('/home'); ``` 

#### assertPathIsNot

Assert that the current path does not match the given path:

```php $browser->assertPathIsNot('/home'); ``` 

#### assertRouteIs

Assert that the current URL matches the given [named route's](/docs/12.x/routing#named-routes) URL:

```php $browser->assertRouteIs($name, $parameters); ``` 

#### assertQueryStringHas

Assert that the given query string parameter is present:

```php $browser->assertQueryStringHas($name); ``` 

Assert that the given query string parameter is present and has a given value:

```php $browser->assertQueryStringHas($name, $value); ``` 

#### assertQueryStringMissing

Assert that the given query string parameter is missing:

```php $browser->assertQueryStringMissing($name); ``` 

#### assertFragmentIs

Assert that the URL's current hash fragment matches the given fragment:

```php $browser->assertFragmentIs('anchor'); ``` 

#### assertFragmentBeginsWith

Assert that the URL's current hash fragment begins with the given fragment:

```php $browser->assertFragmentBeginsWith('anchor'); ``` 

#### assertFragmentIsNot

Assert that the URL's current hash fragment does not match the given fragment:

```php $browser->assertFragmentIsNot('anchor'); ``` 

#### assertHasCookie

Assert that the given encrypted cookie is present:

```php $browser->assertHasCookie($name); ``` 

#### assertHasPlainCookie

Assert that the given unencrypted cookie is present:

```php $browser->assertHasPlainCookie($name); ``` 

#### assertCookieMissing

Assert that the given encrypted cookie is not present:

```php $browser->assertCookieMissing($name); ``` 

#### assertPlainCookieMissing

Assert that the given unencrypted cookie is not present:

```php $browser->assertPlainCookieMissing($name); ``` 

#### assertCookieValue

Assert that an encrypted cookie has a given value:

```php $browser->assertCookieValue($name, $value); ``` 

#### assertPlainCookieValue

Assert that an unencrypted cookie has a given value:

```php $browser->assertPlainCookieValue($name, $value); ``` 

#### assertSee

Assert that the given text is present on the page:

```php $browser->assertSee($text); ``` 

#### assertDontSee

Assert that the given text is not present on the page:

```php $browser->assertDontSee($text); ``` 

#### assertSeeIn

Assert that the given text is present within the selector:

```php $browser->assertSeeIn($selector, $text); ``` 

#### assertDontSeeIn

Assert that the given text is not present within the selector:

```php $browser->assertDontSeeIn($selector, $text); ``` 

#### assertSeeAnythingIn

Assert that any text is present within the selector:

```php $browser->assertSeeAnythingIn($selector); ``` 

#### assertSeeNothingIn

Assert that no text is present within the selector:

```php $browser->assertSeeNothingIn($selector); ``` 

#### assertCount

Assert that elements matching the given selector appear the specified number of times:

```php $browser->assertCount($selector, $count); ``` 

#### assertScript

Assert that the given JavaScript expression evaluates to the given value:

```php $browser->assertScript('window.isLoaded') ->assertScript('document.readyState', 'complete'); ``` 

#### assertSourceHas

Assert that the given source code is present on the page:

```php $browser->assertSourceHas($code); ``` 

#### assertSourceMissing

Assert that the given source code is not present on the page:

```php $browser->assertSourceMissing($code); ``` 

#### assertSeeLink

Assert that the given link is present on the page:

```php $browser->assertSeeLink($linkText); ``` 

#### assertDontSeeLink

Assert that the given link is not present on the page:

```php $browser->assertDontSeeLink($linkText); ``` 

#### assertInputValue

Assert that the given input field has the given value:

```php $browser->assertInputValue($field, $value); ``` 

#### assertInputValueIsNot

Assert that the given input field does not have the given value:

```php $browser->assertInputValueIsNot($field, $value); ``` 

#### assertChecked

Assert that the given checkbox is checked:

```php $browser->assertChecked($field); ``` 

#### assertNotChecked

Assert that the given checkbox is not checked:

```php $browser->assertNotChecked($field); ``` 

#### assertIndeterminate

Assert that the given checkbox is in an indeterminate state:

```php $browser->assertIndeterminate($field); ``` 

#### assertRadioSelected

Assert that the given radio field is selected:

```php $browser->assertRadioSelected($field, $value); ``` 

#### assertRadioNotSelected

Assert that the given radio field is not selected:

```php $browser->assertRadioNotSelected($field, $value); ``` 

#### assertSelected

Assert that the given dropdown has the given value selected:

```php $browser->assertSelected($field, $value); ``` 

#### assertNotSelected

Assert that the given dropdown does not have the given value selected:

```php $browser->assertNotSelected($field, $value); ``` 

#### assertSelectHasOptions

Assert that the given array of values are available to be selected:

```php $browser->assertSelectHasOptions($field, $values); ``` 

#### assertSelectMissingOptions

Assert that the given array of values are not available to be selected:

```php $browser->assertSelectMissingOptions($field, $values); ``` 

#### assertSelectHasOption

Assert that the given value is available to be selected on the given field:

```php $browser->assertSelectHasOption($field, $value); ``` 

#### assertSelectMissingOption

Assert that the given value is not available to be selected:

```php $browser->assertSelectMissingOption($field, $value); ``` 

#### assertValue

Assert that the element matching the given selector has the given value:

```php $browser->assertValue($selector, $value); ``` 

#### assertValueIsNot

Assert that the element matching the given selector does not have the given value:

```php $browser->assertValueIsNot($selector, $value); ``` 

#### assertAttribute

Assert that the element matching the given selector has the given value in the provided attribute:

```php $browser->assertAttribute($selector, $attribute, $value); ``` 

#### assertAttributeMissing

Assert that the element matching the given selector is missing the provided attribute:

```php $browser->assertAttributeMissing($selector, $attribute); ``` 

#### assertAttributeContains

Assert that the element matching the given selector contains the given value in the provided attribute:

```php $browser->assertAttributeContains($selector, $attribute, $value); ``` 

#### assertAttributeDoesntContain

Assert that the element matching the given selector does not contain the given value in the provided attribute:

```php $browser->assertAttributeDoesntContain($selector, $attribute, $value); ``` 

#### assertAriaAttribute

Assert that the element matching the given selector has the given value in the provided aria attribute:

```php $browser->assertAriaAttribute($selector, $attribute, $value); ``` 

For example, given the markup `<button aria-label="Add"></button>`, you may assert against the `aria-label` attribute like so:

```php $browser->assertAriaAttribute('button', 'label', 'Add') ``` 

#### assertDataAttribute

Assert that the element matching the given selector has the given value in the provided data attribute:

```php $browser->assertDataAttribute($selector, $attribute, $value); ``` 

For example, given the markup `<tr id="row-1" data-content="attendees"></tr>`, you may assert against the `data-label` attribute like so:

```php $browser->assertDataAttribute('#row-1', 'content', 'attendees') ``` 

#### assertVisible

Assert that the element matching the given selector is visible:

```php $browser->assertVisible($selector); ``` 

#### assertPresent

Assert that the element matching the given selector is present in the source:

```php $browser->assertPresent($selector); ``` 

#### assertNotPresent

Assert that the element matching the given selector is not present in the source:

```php $browser->assertNotPresent($selector); ``` 

#### assertMissing

Assert that the element matching the given selector is not visible:

```php $browser->assertMissing($selector); ``` 

#### assertInputPresent

Assert that an input with the given name is present:

```php $browser->assertInputPresent($name); ``` 

#### assertInputMissing

Assert that an input with the given name is not present in the source:

```php $browser->assertInputMissing($name); ``` 

#### assertDialogOpened

Assert that a JavaScript dialog with the given message has been opened:

```php $browser->assertDialogOpened($message); ``` 

#### assertEnabled

Assert that the given field is enabled:

```php $browser->assertEnabled($field); ``` 

#### assertDisabled

Assert that the given field is disabled:

```php $browser->assertDisabled($field); ``` 

#### assertButtonEnabled

Assert that the given button is enabled:

```php $browser->assertButtonEnabled($button); ``` 

#### assertButtonDisabled

Assert that the given button is disabled:

```php $browser->assertButtonDisabled($button); ``` 

#### assertFocused

Assert that the given field is focused:

```php $browser->assertFocused($field); ``` 

#### assertNotFocused

Assert that the given field is not focused:

```php $browser->assertNotFocused($field); ``` 

#### assertAuthenticated

Assert that the user is authenticated:

```php $browser->assertAuthenticated(); ``` 

#### assertGuest

Assert that the user is not authenticated:

```php $browser->assertGuest(); ``` 

#### assertAuthenticatedAs

Assert that the user is authenticated as the given user:

```php $browser->assertAuthenticatedAs($user); ``` 

#### assertVue

Dusk even allows you to make assertions on the state of [Vue component](https://vuejs.org) data. For example, imagine your application contains the following Vue component:
    
    
     1// HTML...
    
     2 
    
     3<profile dusk="profile-component"></profile>
    
     4 
    
     5// Component Definition...
    
     6 
    
     7Vue.component('profile', {
    
     8    template: '<div>{{ user.name }}</div>',
    
     9 
    
    10    data: function () {
    
    11        return {
    
    12            user: {
    
    13                name: 'Taylor'
    
    14            }
    
    15        };
    
    16    }
    
    17});
    
    
    // HTML...
    
    <profile dusk="profile-component"></profile>
    
    // Component Definition...
    
    Vue.component('profile', {
        template: '<div>{{ user.name }}</div>',
    
        data: function () {
            return {
                user: {
                    name: 'Taylor'
                }
            };
        }
    });

You may assert on the state of the Vue component like so:

Pest PHPUnit

```php test('vue', function () { $this->browse(function (Browser $browser) { $browser->visit('/') ->assertVue('user.name', 'Taylor', '@profile-component'); }); }); ``` ```php /** * A basic Vue test example. */ public function test_vue(): void { $this->browse(function (Browser $browser) { $browser->visit('/') ->assertVue('user.name', 'Taylor', '@profile-component'); }); } ``` 

#### assertVueIsNot

Assert that a given Vue component data property does not match the given value:

```php $browser->assertVueIsNot($property, $value, $componentSelector = null); ``` 

#### assertVueContains

Assert that a given Vue component data property is an array and contains the given value:

```php $browser->assertVueContains($property, $value, $componentSelector = null); ``` 

#### assertVueDoesntContain

Assert that a given Vue component data property is an array and does not contain the given value:

```php $browser->assertVueDoesntContain($property, $value, $componentSelector = null); ``` 

## Pages

Sometimes, tests require several complicated actions to be performed in sequence. This can make your tests harder to read and understand. Dusk Pages allow you to define expressive actions that may then be performed on a given page via a single method. Pages also allow you to define short-cuts to common selectors for your application or for a single page.

### Generating Pages

To generate a page object, execute the `dusk:page` Artisan command. All page objects will be placed in your application's `tests/Browser/Pages` directory:

```shell php artisan dusk:page Login ``` 

### Configuring Pages

By default, pages have three methods: `url`, `assert`, and `elements`. We will discuss the `url` and `assert` methods now. The `elements` method will be discussed in more detail below.

#### The `url` Method

The `url` method should return the path of the URL that represents the page. Dusk will use this URL when navigating to the page in the browser:

```php /** * Get the URL for the page. */ public function url(): string { return '/login'; } ``` 

#### The `assert` Method

The `assert` method may make any assertions necessary to verify that the browser is actually on the given page. It is not actually necessary to place anything within this method; however, you are free to make these assertions if you wish. These assertions will be run automatically when navigating to the page:

```php /** * Assert that the browser is on the page. */ public function assert(Browser $browser): void { $browser->assertPathIs($this->url()); } ``` 

### Navigating to Pages

Once a page has been defined, you may navigate to it using the `visit` method:

```php use Tests\Browser\Pages\Login; $browser->visit(new Login); ``` 

Sometimes you may already be on a given page and need to "load" the page's selectors and methods into the current test context. This is common when pressing a button and being redirected to a given page without explicitly navigating to it. In this situation, you may use the `on` method to load the page:

```php use Tests\Browser\Pages\CreatePlaylist; $browser->visit('/dashboard') ->clickLink('Create Playlist') ->on(new CreatePlaylist) ->assertSee('@create'); ``` 

### Shorthand Selectors

The `elements` method within page classes allows you to define quick, easy-to-remember shortcuts for any CSS selector on your page. For example, let's define a shortcut for the "email" input field of the application's login page:

```php /** * Get the element shortcuts for the page. * * @return array<string, string> */ public function elements(): array { return [ '@email' => 'input[name=email]', ]; } ``` 

Once the shortcut has been defined, you may use the shorthand selector anywhere you would typically use a full CSS selector:

```php $browser->type('@email', '[email protected]'); ``` 

#### Global Shorthand Selectors

After installing Dusk, a base `Page` class will be placed in your `tests/Browser/Pages` directory. This class contains a `siteElements` method which may be used to define global shorthand selectors that should be available on every page throughout your application:

```php /** * Get the global element shortcuts for the site. * * @return array<string, string> */ public static function siteElements(): array { return [ '@element' => '#selector', ]; } ``` 

### Page Methods

In addition to the default methods defined on pages, you may define additional methods which may be used throughout your tests. For example, let's imagine we are building a music management application. A common action for one page of the application might be to create a playlist. Instead of re-writing the logic to create a playlist in each test, you may define a `createPlaylist` method on a page class:

```php <?php namespace Tests\Browser\Pages; use Laravel\Dusk\Browser; use Laravel\Dusk\Page; class Dashboard extends Page { // Other page methods... /** * Create a new playlist. */ public function createPlaylist(Browser $browser, string $name): void { $browser->type('name', $name) ->check('share') ->press('Create Playlist'); } } ``` 

Once the method has been defined, you may use it within any test that utilizes the page. The browser instance will automatically be passed as the first argument to custom page methods:

```php use Tests\Browser\Pages\Dashboard; $browser->visit(new Dashboard) ->createPlaylist('My Playlist') ->assertSee('My Playlist'); ``` 

## Components

Components are similar to Dusk’s “page objects”, but are intended for pieces of UI and functionality that are re-used throughout your application, such as a navigation bar or notification window. As such, components are not bound to specific URLs.

### Generating Components

To generate a component, execute the `dusk:component` Artisan command. New components are placed in the `tests/Browser/Components` directory:

```shell php artisan dusk:component DatePicker ``` 

As shown above, a "date picker" is an example of a component that might exist throughout your application on a variety of pages. It can become cumbersome to manually write the browser automation logic to select a date in dozens of tests throughout your test suite. Instead, we can define a Dusk component to represent the date picker, allowing us to encapsulate that logic within the component:

```php <?php namespace Tests\Browser\Components; use Laravel\Dusk\Browser; use Laravel\Dusk\Component as BaseComponent; class DatePicker extends BaseComponent { /** * Get the root selector for the component. */ public function selector(): string { return '.date-picker'; } /** * Assert that the browser page contains the component. */ public function assert(Browser $browser): void { $browser->assertVisible($this->selector()); } /** * Get the element shortcuts for the component. * * @return array<string, string> */ public function elements(): array { return [ '@date-field' => 'input.datepicker-input', '@year-list' => 'div > div.datepicker-years', '@month-list' => 'div > div.datepicker-months', '@day-list' => 'div > div.datepicker-days', ]; } /** * Select the given date. */ public function selectDate(Browser $browser, int $year, int $month, int $day): void { $browser->click('@date-field') ->within('@year-list', function (Browser $browser) use ($year) { $browser->click($year); }) ->within('@month-list', function (Browser $browser) use ($month) { $browser->click($month); }) ->within('@day-list', function (Browser $browser) use ($day) { $browser->click($day); }); } } ``` 

### Using Components

Once the component has been defined, we can easily select a date within the date picker from any test. And, if the logic necessary to select a date changes, we only need to update the component:

Pest PHPUnit

```php <?php use Illuminate\Foundation\Testing\DatabaseMigrations; use Laravel\Dusk\Browser; use Tests\Browser\Components\DatePicker; uses(DatabaseMigrations::class); test('basic example', function () { $this->browse(function (Browser $browser) { $browser->visit('/') ->within(new DatePicker, function (Browser $browser) { $browser->selectDate(2019, 1, 30); }) ->assertSee('January'); }); }); ``` ```php <?php namespace Tests\Browser; use Illuminate\Foundation\Testing\DatabaseMigrations; use Laravel\Dusk\Browser; use Tests\Browser\Components\DatePicker; use Tests\DuskTestCase; class ExampleTest extends DuskTestCase { /** * A basic component test example. */ public function test_basic_example(): void { $this->browse(function (Browser $browser) { $browser->visit('/') ->within(new DatePicker, function (Browser $browser) { $browser->selectDate(2019, 1, 30); }) ->assertSee('January'); }); } } ``` 

The `component` method may be used to retrieve a browser instance scoped to the given component:

```php $datePicker = $browser->component(new DatePickerComponent); $datePicker->selectDate(2019, 1, 30); $datePicker->assertSee('January'); ``` 

## Continuous Integration

Most Dusk continuous integration configurations expect your Laravel application to be served using the built-in PHP development server on port 8000. Therefore, before continuing, you should ensure that your continuous integration environment has an `APP_URL` environment variable value of `http://127.0.0.1:8000`.

### Heroku CI

To run Dusk tests on [Heroku CI](https://www.heroku.com/continuous-integration), add the following Google Chrome buildpack and scripts to your Heroku `app.json` file:

```json { "environments": { "test": { "buildpacks": [ { "url": "heroku/php" }, { "url": "https://github.com/heroku/heroku-buildpack-chrome-for-testing" } ], "scripts": { "test-setup": "cp .env.testing .env", "test": "nohup bash -c './vendor/laravel/dusk/bin/chromedriver-linux --port=9515 > /dev/null 2>&1 &' && nohup bash -c 'php artisan serve --no-reload > /dev/null 2>&1 &' && php artisan dusk" } } } } ``` 

### Travis CI

To run your Dusk tests on [Travis CI](https://travis-ci.org), use the following `.travis.yml` configuration. Since Travis CI is not a graphical environment, we will need to take some extra steps in order to launch a Chrome browser. In addition, we will use `php artisan serve` to launch PHP's built-in web server:

```yaml language: php php: \- 8.2 addons: chrome: stable install: \- cp .env.testing .env \- travis_retry composer install --no-interaction --prefer-dist \- php artisan key:generate \- php artisan dusk:chrome-driver before_script: \- google-chrome-stable --headless --disable-gpu --remote-debugging-port=9222 http://localhost & \- php artisan serve --no-reload & script: \- php artisan dusk ``` 

### GitHub Actions

If you are using [GitHub Actions](https://github.com/features/actions) to run your Dusk tests, you may use the following configuration file as a starting point. Like TravisCI, we will use the `php artisan serve` command to launch PHP's built-in web server:

```yaml name: CI on: [push] jobs: dusk-php: runs-on: ubuntu-latest env: APP_URL: "http://127.0.0.1:8000" DB_USERNAME: root DB_PASSWORD: root MAIL_MAILER: log steps: \- uses: actions/checkout@v4 \- name: Prepare The Environment run: cp .env.example .env \- name: Create Database run: | sudo systemctl start mysql mysql --user="root" --password="root" -e "CREATE DATABASE \\`my-database\\` character set UTF8mb4 collate utf8mb4_bin;" \- name: Install Composer Dependencies run: composer install --no-progress --prefer-dist --optimize-autoloader \- name: Generate Application Key run: php artisan key:generate \- name: Upgrade Chrome Driver run: php artisan dusk:chrome-driver --detect \- name: Start Chrome Driver run: ./vendor/laravel/dusk/bin/chromedriver-linux --port=9515 & \- name: Run Laravel Server run: php artisan serve --no-reload & \- name: Run Dusk Tests run: php artisan dusk \- name: Upload Screenshots if: failure() uses: actions/upload-artifact@v4 with: name: screenshots path: tests/Browser/screenshots \- name: Upload Console Logs if: failure() uses: actions/upload-artifact@v4 with: name: console path: tests/Browser/console ``` 

### Chipper CI

If you are using [Chipper CI](https://chipperci.com) to run your Dusk tests, you may use the following configuration file as a starting point. We will use PHP's built-in server to run Laravel so we can listen for requests:

```yaml # file .chipperci.yml version: 1 environment: php: 8.2 node: 16 # Include Chrome in the build environment services: \- dusk # Build all commits on: push: branches: .* pipeline: \- name: Setup cmd: | cp -v .env.example .env composer install --no-interaction --prefer-dist --optimize-autoloader php artisan key:generate # Create a dusk env file, ensuring APP_URL uses BUILD_HOST cp -v .env .env.dusk.ci sed -i "s@APP_URL=.*@APP_URL=http://$BUILD_HOST:8000@g" .env.dusk.ci \- name: Compile Assets cmd: | npm ci --no-audit npm run build \- name: Browser Tests cmd: | php -S [::0]:8000 -t public 2>server.log & sleep 2 php artisan dusk:chrome-driver $CHROME_DRIVER php artisan dusk --env=ci ``` 

To learn more about running Dusk tests on Chipper CI, including how to use databases, consult the [official Chipper CI documentation](https://chipperci.com/docs/testing/laravel-dusk-new/).
