# Source: https://laravel.com/docs/12.x/http-tests

# HTTP Tests

  * Introduction
  * Making Requests
    * Customizing Request Headers
    * Cookies
    * Session / Authentication
    * Debugging Responses
    * Exception Handling
  * Testing JSON APIs
    * Fluent JSON Testing
  * Testing File Uploads
  * Testing Views
    * Rendering Blade and Components
  * Available Assertions
    * Response Assertions
    * Authentication Assertions
    * Validation Assertions



## Introduction

Laravel provides a very fluent API for making HTTP requests to your application and examining the responses. For example, take a look at the feature test defined below:

Pest PHPUnit

```php <?php test('the application returns a successful response', function () { $response = $this->get('/'); $response->assertStatus(200); }); ``` ```php <?php namespace Tests\Feature; use Tests\TestCase; class ExampleTest extends TestCase { /** * A basic test example. */ public function test_the_application_returns_a_successful_response(): void { $response = $this->get('/'); $response->assertStatus(200); } } ``` 

The `get` method makes a `GET` request into the application, while the `assertStatus` method asserts that the returned response should have the given HTTP status code. In addition to this simple assertion, Laravel also contains a variety of assertions for inspecting the response headers, content, JSON structure, and more.

## Making Requests

To make a request to your application, you may invoke the `get`, `post`, `put`, `patch`, or `delete` methods within your test. These methods do not actually issue a "real" HTTP request to your application. Instead, the entire network request is simulated internally.

Instead of returning an `Illuminate\Http\Response` instance, test request methods return an instance of `Illuminate\Testing\TestResponse`, which provides a variety of helpful assertions that allow you to inspect your application's responses:

Pest PHPUnit

```php <?php test('basic request', function () { $response = $this->get('/'); $response->assertStatus(200); }); ``` ```php <?php namespace Tests\Feature; use Tests\TestCase; class ExampleTest extends TestCase { /** * A basic test example. */ public function test_a_basic_request(): void { $response = $this->get('/'); $response->assertStatus(200); } } ``` 

In general, each of your tests should only make one request to your application. Unexpected behavior may occur if multiple requests are executed within a single test method.

For convenience, the CSRF middleware is automatically disabled when running tests.

### Customizing Request Headers

You may use the `withHeaders` method to customize the request's headers before it is sent to the application. This method allows you to add any custom headers you would like to the request:

Pest PHPUnit

```php <?php test('interacting with headers', function () { $response = $this->withHeaders([ 'X-Header' => 'Value', ])->post('/user', ['name' => 'Sally']); $response->assertStatus(201); }); ``` ```php <?php namespace Tests\Feature; use Tests\TestCase; class ExampleTest extends TestCase { /** * A basic functional test example. */ public function test_interacting_with_headers(): void { $response = $this->withHeaders([ 'X-Header' => 'Value', ])->post('/user', ['name' => 'Sally']); $response->assertStatus(201); } } ``` 

### Cookies

You may use the `withCookie` or `withCookies` methods to set cookie values before making a request. The `withCookie` method accepts a cookie name and value as its two arguments, while the `withCookies` method accepts an array of name / value pairs:

Pest PHPUnit

```php <?php test('interacting with cookies', function () { $response = $this->withCookie('color', 'blue')->get('/'); $response = $this->withCookies([ 'color' => 'blue', 'name' => 'Taylor', ])->get('/'); // }); ``` ```php <?php namespace Tests\Feature; use Tests\TestCase; class ExampleTest extends TestCase { public function test_interacting_with_cookies(): void { $response = $this->withCookie('color', 'blue')->get('/'); $response = $this->withCookies([ 'color' => 'blue', 'name' => 'Taylor', ])->get('/'); // } } ``` 

### Session / Authentication

Laravel provides several helpers for interacting with the session during HTTP testing. First, you may set the session data to a given array using the `withSession` method. This is useful for loading the session with data before issuing a request to your application:

Pest PHPUnit

```php <?php test('interacting with the session', function () { $response = $this->withSession(['banned' => false])->get('/'); // }); ``` ```php <?php namespace Tests\Feature; use Tests\TestCase; class ExampleTest extends TestCase { public function test_interacting_with_the_session(): void { $response = $this->withSession(['banned' => false])->get('/'); // } } ``` 

Laravel's session is typically used to maintain state for the currently authenticated user. Therefore, the `actingAs` helper method provides a simple way to authenticate a given user as the current user. For example, we may use a [model factory](/docs/12.x/eloquent-factories) to generate and authenticate a user:

Pest PHPUnit

```php <?php use App\Models\User; test('an action that requires authentication', function () { $user = User::factory()->create(); $response = $this->actingAs($user) ->withSession(['banned' => false]) ->get('/'); // }); ``` ```php <?php namespace Tests\Feature; use App\Models\User; use Tests\TestCase; class ExampleTest extends TestCase { public function test_an_action_that_requires_authentication(): void { $user = User::factory()->create(); $response = $this->actingAs($user) ->withSession(['banned' => false]) ->get('/'); // } } ``` 

You may also specify which guard should be used to authenticate the given user by passing the guard name as the second argument to the `actingAs` method. The guard that is provided to the `actingAs` method will also become the default guard for the duration of the test:

```php $this->actingAs($user, 'web') ``` 

### Debugging Responses

After making a test request to your application, the `dump`, `dumpHeaders`, and `dumpSession` methods may be used to examine and debug the response contents:

Pest PHPUnit

```php <?php test('basic test', function () { $response = $this->get('/'); $response->dumpHeaders(); $response->dumpSession(); $response->dump(); }); ``` ```php <?php namespace Tests\Feature; use Tests\TestCase; class ExampleTest extends TestCase { /** * A basic test example. */ public function test_basic_test(): void { $response = $this->get('/'); $response->dumpHeaders(); $response->dumpSession(); $response->dump(); } } ``` 

Alternatively, you may use the `dd`, `ddHeaders`, `ddBody`, `ddJson`, and `ddSession` methods to dump information about the response and then stop execution:

Pest PHPUnit

```php <?php test('basic test', function () { $response = $this->get('/'); $response->dd(); $response->ddHeaders(); $response->ddBody(); $response->ddJson(); $response->ddSession(); }); ``` ```php <?php namespace Tests\Feature; use Tests\TestCase; class ExampleTest extends TestCase { /** * A basic test example. */ public function test_basic_test(): void { $response = $this->get('/'); $response->dd(); $response->ddHeaders(); $response->ddBody(); $response->ddJson(); $response->ddSession(); } } ``` 

### Exception Handling

Sometimes you may need to test that your application is throwing a specific exception. To accomplish this, you may "fake" the exception handler via the `Exceptions` facade. Once the exception handler has been faked, you may utilize the `assertReported` and `assertNotReported` methods to make assertions against exceptions that were thrown during the request:

Pest PHPUnit

```php <?php use App\Exceptions\InvalidOrderException; use Illuminate\Support\Facades\Exceptions; test('exception is thrown', function () { Exceptions::fake(); $response = $this->get('/order/1'); // Assert an exception was thrown... Exceptions::assertReported(InvalidOrderException::class); // Assert against the exception... Exceptions::assertReported(function (InvalidOrderException $e) { return $e->getMessage() === 'The order was invalid.'; }); }); ``` ```php <?php namespace Tests\Feature; use App\Exceptions\InvalidOrderException; use Illuminate\Support\Facades\Exceptions; use Tests\TestCase; class ExampleTest extends TestCase { /** * A basic test example. */ public function test_exception_is_thrown(): void { Exceptions::fake(); $response = $this->get('/'); // Assert an exception was thrown... Exceptions::assertReported(InvalidOrderException::class); // Assert against the exception... Exceptions::assertReported(function (InvalidOrderException $e) { return $e->getMessage() === 'The order was invalid.'; }); } } ``` 

The `assertNotReported` and `assertNothingReported` methods may be used to assert that a given exception was not thrown during the request or that no exceptions were thrown:

```php Exceptions::assertNotReported(InvalidOrderException::class); Exceptions::assertNothingReported(); ``` 

You may totally disable exception handling for a given request by invoking the `withoutExceptionHandling` method before making your request:

```php $response = $this->withoutExceptionHandling()->get('/'); ``` 

In addition, if you would like to ensure that your application is not utilizing features that have been deprecated by the PHP language or the libraries your application is using, you may invoke the `withoutDeprecationHandling` method before making your request. When deprecation handling is disabled, deprecation warnings will be converted to exceptions, thus causing your test to fail:

```php $response = $this->withoutDeprecationHandling()->get('/'); ``` 

The `assertThrows` method may be used to assert that code within a given closure throws an exception of the specified type:

```php $this->assertThrows( fn () => (new ProcessOrder)->execute(), OrderInvalid::class ); ``` 

If you would like to inspect and make assertions against the exception that is thrown, you may provide a closure as the second argument to the `assertThrows` method:

```php $this->assertThrows( fn () => (new ProcessOrder)->execute(), fn (OrderInvalid $e) => $e->orderId() === 123; ); ``` 

The `assertDoesntThrow` method may be used to assert that the code within a given closure does not throw any exceptions:

```php $this->assertDoesntThrow(fn () => (new ProcessOrder)->execute()); ``` 

## Testing JSON APIs

Laravel also provides several helpers for testing JSON APIs and their responses. For example, the `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, and `optionsJson` methods may be used to issue JSON requests with various HTTP verbs. You may also easily pass data and headers to these methods. To get started, let's write a test to make a `POST` request to `/api/user` and assert that the expected JSON data was returned:

Pest PHPUnit

```php <?php test('making an api request', function () { $response = $this->postJson('/api/user', ['name' => 'Sally']); $response ->assertStatus(201) ->assertJson([ 'created' => true, ]); }); ``` ```php <?php namespace Tests\Feature; use Tests\TestCase; class ExampleTest extends TestCase { /** * A basic functional test example. */ public function test_making_an_api_request(): void { $response = $this->postJson('/api/user', ['name' => 'Sally']); $response ->assertStatus(201) ->assertJson([ 'created' => true, ]); } } ``` 

In addition, JSON response data may be accessed as array variables on the response, making it convenient for you to inspect the individual values returned within a JSON response:

Pest PHPUnit

```php expect($response['created'])->toBeTrue(); ``` ```php $this->assertTrue($response['created']); ``` 

The `assertJson` method converts the response to an array to verify that the given array exists within the JSON response returned by the application. So, if there are other properties in the JSON response, this test will still pass as long as the given fragment is present.

#### Asserting Exact JSON Matches

As previously mentioned, the `assertJson` method may be used to assert that a fragment of JSON exists within the JSON response. If you would like to verify that a given array **exactly matches** the JSON returned by your application, you should use the `assertExactJson` method:

Pest PHPUnit

```php <?php test('asserting an exact json match', function () { $response = $this->postJson('/user', ['name' => 'Sally']); $response ->assertStatus(201) ->assertExactJson([ 'created' => true, ]); }); ``` ```php <?php namespace Tests\Feature; use Tests\TestCase; class ExampleTest extends TestCase { /** * A basic functional test example. */ public function test_asserting_an_exact_json_match(): void { $response = $this->postJson('/user', ['name' => 'Sally']); $response ->assertStatus(201) ->assertExactJson([ 'created' => true, ]); } } ``` 

#### Asserting on JSON Paths

If you would like to verify that the JSON response contains the given data at a specified path, you should use the `assertJsonPath` method:

Pest PHPUnit

```php <?php test('asserting a json path value', function () { $response = $this->postJson('/user', ['name' => 'Sally']); $response ->assertStatus(201) ->assertJsonPath('team.owner.name', 'Darian'); }); ``` ```php <?php namespace Tests\Feature; use Tests\TestCase; class ExampleTest extends TestCase { /** * A basic functional test example. */ public function test_asserting_a_json_paths_value(): void { $response = $this->postJson('/user', ['name' => 'Sally']); $response ->assertStatus(201) ->assertJsonPath('team.owner.name', 'Darian'); } } ``` 

The `assertJsonPath` method also accepts a closure, which may be used to dynamically determine if the assertion should pass:

```php $response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3); ``` 

### Fluent JSON Testing

Laravel also offers a beautiful way to fluently test your application's JSON responses. To get started, pass a closure to the `assertJson` method. This closure will be invoked with an instance of `Illuminate\Testing\Fluent\AssertableJson` which can be used to make assertions against the JSON that was returned by your application. The `where` method may be used to make assertions against a particular attribute of the JSON, while the `missing` method may be used to assert that a particular attribute is missing from the JSON:

Pest PHPUnit

```php use Illuminate\Testing\Fluent\AssertableJson; test('fluent json', function () { $response = $this->getJson('/users/1'); $response ->assertJson(fn (AssertableJson $json) => $json->where('id', 1) ->where('name', 'Victoria Faith') ->where('email', fn (string $email) => str($email)->is('[email protected]')) ->whereNot('status', 'pending') ->missing('password') ->etc() ); }); ``` ```php use Illuminate\Testing\Fluent\AssertableJson; /** * A basic functional test example. */ public function test_fluent_json(): void { $response = $this->getJson('/users/1'); $response ->assertJson(fn (AssertableJson $json) => $json->where('id', 1) ->where('name', 'Victoria Faith') ->where('email', fn (string $email) => str($email)->is('[email protected]')) ->whereNot('status', 'pending') ->missing('password') ->etc() ); } ``` 

#### Understanding the `etc` Method

In the example above, you may have noticed we invoked the `etc` method at the end of our assertion chain. This method informs Laravel that there may be other attributes present on the JSON object. If the `etc` method is not used, the test will fail if other attributes that you did not make assertions against exist on the JSON object.

The intention behind this behavior is to protect you from unintentionally exposing sensitive information in your JSON responses by forcing you to either explicitly make an assertion against the attribute or explicitly allow additional attributes via the `etc` method.

However, you should be aware that not including the `etc` method in your assertion chain does not ensure that additional attributes are not being added to arrays that are nested within your JSON object. The `etc` method only ensures that no additional attributes exist at the nesting level in which the `etc` method is invoked.

#### Asserting Attribute Presence / Absence

To assert that an attribute is present or absent, you may use the `has` and `missing` methods:

```php $response->assertJson(fn (AssertableJson $json) => $json->has('data') ->missing('message') ); ``` 

In addition, the `hasAll` and `missingAll` methods allow asserting the presence or absence of multiple attributes simultaneously:

```php $response->assertJson(fn (AssertableJson $json) => $json->hasAll(['status', 'data']) ->missingAll(['message', 'code']) ); ``` 

You may use the `hasAny` method to determine if at least one of a given list of attributes is present:

```php $response->assertJson(fn (AssertableJson $json) => $json->has('status') ->hasAny('data', 'message', 'code') ); ``` 

#### Asserting Against JSON Collections

Often, your route will return a JSON response that contains multiple items, such as multiple users:

```php Route::get('/users', function () { return User::all(); }); ``` 

In these situations, we may use the fluent JSON object's `has` method to make assertions against the users included in the response. For example, let's assert that the JSON response contains three users. Next, we'll make some assertions about the first user in the collection using the `first` method. The `first` method accepts a closure which receives another assertable JSON string that we can use to make assertions about the first object in the JSON collection:

```php $response ->assertJson(fn (AssertableJson $json) => $json->has(3) ->first(fn (AssertableJson $json) => $json->where('id', 1) ->where('name', 'Victoria Faith') ->where('email', fn (string $email) => str($email)->is('[email protected]')) ->missing('password') ->etc() ) ); ``` 

#### Scoping JSON Collection Assertions

Sometimes, your application's routes will return JSON collections that are assigned named keys:

```php Route::get('/users', function () { return [ 'meta' => [...], 'users' => User::all(), ]; }) ``` 

When testing these routes, you may use the `has` method to assert against the number of items in the collection. In addition, you may use the `has` method to scope a chain of assertions:

```php $response ->assertJson(fn (AssertableJson $json) => $json->has('meta') ->has('users', 3) ->has('users.0', fn (AssertableJson $json) => $json->where('id', 1) ->where('name', 'Victoria Faith') ->where('email', fn (string $email) => str($email)->is('[email protected]')) ->missing('password') ->etc() ) ); ``` 

However, instead of making two separate calls to the `has` method to assert against the `users` collection, you may make a single call which provides a closure as its third parameter. When doing so, the closure will automatically be invoked and scoped to the first item in the collection:

```php $response ->assertJson(fn (AssertableJson $json) => $json->has('meta') ->has('users', 3, fn (AssertableJson $json) => $json->where('id', 1) ->where('name', 'Victoria Faith') ->where('email', fn (string $email) => str($email)->is('[email protected]')) ->missing('password') ->etc() ) ); ``` 

#### Asserting JSON Types

You may only want to assert that the properties in the JSON response are of a certain type. The `Illuminate\Testing\Fluent\AssertableJson` class provides the `whereType` and `whereAllType` methods for doing just that:

```php $response->assertJson(fn (AssertableJson $json) => $json->whereType('id', 'integer') ->whereAllType([ 'users.0.name' => 'string', 'meta' => 'array' ]) ); ``` 

You may specify multiple types using the `|` character, or passing an array of types as the second parameter to the `whereType` method. The assertion will be successful if the response value is any of the listed types:

```php $response->assertJson(fn (AssertableJson $json) => $json->whereType('name', 'string|null') ->whereType('id', ['string', 'integer']) ); ``` 

The `whereType` and `whereAllType` methods recognize the following types: `string`, `integer`, `double`, `boolean`, `array`, and `null`.

## Testing File Uploads

The `Illuminate\Http\UploadedFile` class provides a `fake` method which may be used to generate dummy files or images for testing. This, combined with the `Storage` facade's `fake` method, greatly simplifies the testing of file uploads. For example, you may combine these two features to easily test an avatar upload form:

Pest PHPUnit

```php <?php use Illuminate\Http\UploadedFile; use Illuminate\Support\Facades\Storage; test('avatars can be uploaded', function () { Storage::fake('avatars'); $file = UploadedFile::fake()->image('avatar.jpg'); $response = $this->post('/avatar', [ 'avatar' => $file, ]); Storage::disk('avatars')->assertExists($file->hashName()); }); ``` ```php <?php namespace Tests\Feature; use Illuminate\Http\UploadedFile; use Illuminate\Support\Facades\Storage; use Tests\TestCase; class ExampleTest extends TestCase { public function test_avatars_can_be_uploaded(): void { Storage::fake('avatars'); $file = UploadedFile::fake()->image('avatar.jpg'); $response = $this->post('/avatar', [ 'avatar' => $file, ]); Storage::disk('avatars')->assertExists($file->hashName()); } } ``` 

If you would like to assert that a given file does not exist, you may use the `assertMissing` method provided by the `Storage` facade:

```php Storage::fake('avatars'); // ... Storage::disk('avatars')->assertMissing('missing.jpg'); ``` 

#### Fake File Customization

When creating files using the `fake` method provided by the `UploadedFile` class, you may specify the width, height, and size of the image (in kilobytes) in order to better test your application's validation rules:

```php UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100); ``` 

In addition to creating images, you may create files of any other type using the `create` method:

```php UploadedFile::fake()->create('document.pdf', $sizeInKilobytes); ``` 

If needed, you may pass a `$mimeType` argument to the method to explicitly define the MIME type that should be returned by the file:

```php UploadedFile::fake()->create( 'document.pdf', $sizeInKilobytes, 'application/pdf' ); ``` 

## Testing Views

Laravel also allows you to render a view without making a simulated HTTP request to the application. To accomplish this, you may call the `view` method within your test. The `view` method accepts the view name and an optional array of data. The method returns an instance of `Illuminate\Testing\TestView`, which offers several methods to conveniently make assertions about the view's contents:

Pest PHPUnit

```php <?php test('a welcome view can be rendered', function () { $view = $this->view('welcome', ['name' => 'Taylor']); $view->assertSee('Taylor'); }); ``` ```php <?php namespace Tests\Feature; use Tests\TestCase; class ExampleTest extends TestCase { public function test_a_welcome_view_can_be_rendered(): void { $view = $this->view('welcome', ['name' => 'Taylor']); $view->assertSee('Taylor'); } } ``` 

The `TestView` class provides the following assertion methods: `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, and `assertDontSeeText`.

If needed, you may get the raw, rendered view contents by casting the `TestView` instance to a string:

```php $contents = (string) $this->view('welcome'); ``` 

#### Sharing Errors

Some views may depend on errors shared in the [global error bag provided by Laravel](/docs/12.x/validation#quick-displaying-the-validation-errors). To hydrate the error bag with error messages, you may use the `withViewErrors` method:

```php $view = $this->withViewErrors([ 'name' => ['Please provide a valid name.'] ])->view('form'); $view->assertSee('Please provide a valid name.'); ``` 

### Rendering Blade and Components

If necessary, you may use the `blade` method to evaluate and render a raw [Blade](/docs/12.x/blade) string. Like the `view` method, the `blade` method returns an instance of `Illuminate\Testing\TestView`:

```php $view = $this->blade( '<x-component :name="$name" />', ['name' => 'Taylor'] ); $view->assertSee('Taylor'); ``` 

You may use the `component` method to evaluate and render a [Blade component](/docs/12.x/blade#components). The `component` method returns an instance of `Illuminate\Testing\TestComponent`:

```php $view = $this->component(Profile::class, ['name' => 'Taylor']); $view->assertSee('Taylor'); ``` 

## Available Assertions

### Response Assertions

Laravel's `Illuminate\Testing\TestResponse` class provides a variety of custom assertion methods that you may utilize when testing your application. These assertions may be accessed on the response that is returned by the `json`, `get`, `post`, `put`, and `delete` test methods:

assertAccepted assertBadRequest assertClientError assertConflict assertCookie assertCookieExpired assertCookieNotExpired assertCookieMissing assertCreated assertDontSee assertDontSeeText assertDownload assertExactJson assertExactJsonStructure assertForbidden assertFound assertGone assertHeader assertHeaderMissing assertInternalServerError assertJson assertJsonCount assertJsonFragment assertJsonIsArray assertJsonIsObject assertJsonMissing assertJsonMissingExact assertJsonMissingValidationErrors assertJsonPath assertJsonMissingPath assertJsonStructure assertJsonValidationErrors assertJsonValidationErrorFor assertLocation assertMethodNotAllowed assertMovedPermanently assertContent assertNoContent assertStreamed assertStreamedContent assertNotFound assertOk assertPaymentRequired assertPlainCookie assertRedirect assertRedirectBack assertRedirectBackWithErrors assertRedirectBackWithoutErrors assertRedirectContains assertRedirectToRoute assertRedirectToSignedRoute assertRequestTimeout assertSee assertSeeInOrder assertSeeText assertSeeTextInOrder assertServerError assertServiceUnavailable assertSessionHas assertSessionHasInput assertSessionHasAll assertSessionHasErrors assertSessionHasErrorsIn assertSessionHasNoErrors assertSessionDoesntHaveErrors assertSessionMissing assertStatus assertSuccessful assertTooManyRequests assertUnauthorized assertUnprocessable assertUnsupportedMediaType assertValid assertInvalid assertViewHas assertViewHasAll assertViewIs assertViewMissing

#### assertAccepted

Assert that the response has an accepted (202) HTTP status code:

```php $response->assertAccepted(); ``` 

#### assertBadRequest

Assert that the response has a bad request (400) HTTP status code:

```php $response->assertBadRequest(); ``` 

#### assertClientError

Assert that the response has a client error (>= 400, < 500) HTTP status code:

```php $response->assertClientError(); ``` 

#### assertConflict

Assert that the response has a conflict (409) HTTP status code:

```php $response->assertConflict(); ``` 

#### assertCookie

Assert that the response contains the given cookie:

```php $response->assertCookie($cookieName, $value = null); ``` 

#### assertCookieExpired

Assert that the response contains the given cookie and it is expired:

```php $response->assertCookieExpired($cookieName); ``` 

#### assertCookieNotExpired

Assert that the response contains the given cookie and it is not expired:

```php $response->assertCookieNotExpired($cookieName); ``` 

#### assertCookieMissing

Assert that the response does not contain the given cookie:

```php $response->assertCookieMissing($cookieName); ``` 

#### assertCreated

Assert that the response has a 201 HTTP status code:

```php $response->assertCreated(); ``` 

#### assertDontSee

Assert that the given string is not contained within the response returned by the application. This assertion will automatically escape the given string unless you pass a second argument of `false`:

```php $response->assertDontSee($value, $escape = true); ``` 

#### assertDontSeeText

Assert that the given string is not contained within the response text. This assertion will automatically escape the given string unless you pass a second argument of `false`. This method will pass the response content to the `strip_tags` PHP function before making the assertion:

```php $response->assertDontSeeText($value, $escape = true); ``` 

#### assertDownload

Assert that the response is a "download". Typically, this means the invoked route that returned the response returned a `Response::download` response, `BinaryFileResponse`, or `Storage::download` response:

```php $response->assertDownload(); ``` 

If you wish, you may assert that the downloadable file was assigned a given file name:

```php $response->assertDownload('image.jpg'); ``` 

#### assertExactJson

Assert that the response contains an exact match of the given JSON data:

```php $response->assertExactJson(array $data); ``` 

#### assertExactJsonStructure

Assert that the response contains an exact match of the given JSON structure:

```php $response->assertExactJsonStructure(array $data); ``` 

This method is a more strict variant of assertJsonStructure. In contrast with `assertJsonStructure`, this method will fail if the response contains any keys that aren't explicitly included in the expected JSON structure.

#### assertForbidden

Assert that the response has a forbidden (403) HTTP status code:

```php $response->assertForbidden(); ``` 

#### assertFound

Assert that the response has a found (302) HTTP status code:

```php $response->assertFound(); ``` 

#### assertGone

Assert that the response has a gone (410) HTTP status code:

```php $response->assertGone(); ``` 

#### assertHeader

Assert that the given header and value is present on the response:

```php $response->assertHeader($headerName, $value = null); ``` 

#### assertHeaderMissing

Assert that the given header is not present on the response:

```php $response->assertHeaderMissing($headerName); ``` 

#### assertInternalServerError

Assert that the response has an "Internal Server Error" (500) HTTP status code:

```php $response->assertInternalServerError(); ``` 

#### assertJson

Assert that the response contains the given JSON data:

```php $response->assertJson(array $data, $strict = false); ``` 

The `assertJson` method converts the response to an array to verify that the given array exists within the JSON response returned by the application. So, if there are other properties in the JSON response, this test will still pass as long as the given fragment is present.

#### assertJsonCount

Assert that the response JSON has an array with the expected number of items at the given key:

```php $response->assertJsonCount($count, $key = null); ``` 

#### assertJsonFragment

Assert that the response contains the given JSON data anywhere in the response:

```php Route::get('/users', function () { return [ 'users' => [ [ 'name' => 'Taylor Otwell', ], ], ]; }); $response->assertJsonFragment(['name' => 'Taylor Otwell']); ``` 

#### assertJsonIsArray

Assert that the response JSON is an array:

```php $response->assertJsonIsArray(); ``` 

#### assertJsonIsObject

Assert that the response JSON is an object:

```php $response->assertJsonIsObject(); ``` 

#### assertJsonMissing

Assert that the response does not contain the given JSON data:

```php $response->assertJsonMissing(array $data); ``` 

#### assertJsonMissingExact

Assert that the response does not contain the exact JSON data:

```php $response->assertJsonMissingExact(array $data); ``` 

#### assertJsonMissingValidationErrors

Assert that the response has no JSON validation errors for the given keys:

```php $response->assertJsonMissingValidationErrors($keys); ``` 

The more generic assertValid method may be used to assert that a response does not have validation errors that were returned as JSON **and** that no errors were flashed to session storage.

#### assertJsonPath

Assert that the response contains the given data at the specified path:

```php $response->assertJsonPath($path, $expectedValue); ``` 

For example, if the following JSON response is returned by your application:

```json { "user": { "name": "Steve Schoger" } } ``` 

You may assert that the `name` property of the `user` object matches a given value like so:

```php $response->assertJsonPath('user.name', 'Steve Schoger'); ``` 

#### assertJsonMissingPath

Assert that the response does not contain the given path:

```php $response->assertJsonMissingPath($path); ``` 

For example, if the following JSON response is returned by your application:

```json { "user": { "name": "Steve Schoger" } } ``` 

You may assert that it does not contain the `email` property of the `user` object:

```php $response->assertJsonMissingPath('user.email'); ``` 

#### assertJsonStructure

Assert that the response has a given JSON structure:

```php $response->assertJsonStructure(array $structure); ``` 

For example, if the JSON response returned by your application contains the following data:

```json { "user": { "name": "Steve Schoger" } } ``` 

You may assert that the JSON structure matches your expectations like so:

```php $response->assertJsonStructure([ 'user' => [ 'name', ] ]); ``` 

Sometimes, JSON responses returned by your application may contain arrays of objects:

```json { "user": [ { "name": "Steve Schoger", "age": 55, "location": "Earth" }, { "name": "Mary Schoger", "age": 60, "location": "Earth" } ] } ``` 

In this situation, you may use the `*` character to assert against the structure of all of the objects in the array:

```php $response->assertJsonStructure([ 'user' => [ '*' => [ 'name', 'age', 'location' ] ] ]); ``` 

#### assertJsonValidationErrors

Assert that the response has the given JSON validation errors for the given keys. This method should be used when asserting against responses where the validation errors are returned as a JSON structure instead of being flashed to the session:

```php $response->assertJsonValidationErrors(array $data, $responseKey = 'errors'); ``` 

The more generic assertInvalid method may be used to assert that a response has validation errors returned as JSON **or** that errors were flashed to session storage.

#### assertJsonValidationErrorFor

Assert the response has any JSON validation errors for the given key:

```php $response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors'); ``` 

#### assertMethodNotAllowed

Assert that the response has a method not allowed (405) HTTP status code:

```php $response->assertMethodNotAllowed(); ``` 

#### assertMovedPermanently

Assert that the response has a moved permanently (301) HTTP status code:

```php $response->assertMovedPermanently(); ``` 

#### assertLocation

Assert that the response has the given URI value in the `Location` header:

```php $response->assertLocation($uri); ``` 

#### assertContent

Assert that the given string matches the response content:

```php $response->assertContent($value); ``` 

#### assertNoContent

Assert that the response has the given HTTP status code and no content:

```php $response->assertNoContent($status = 204); ``` 

#### assertStreamed

Assert that the response was a streamed response:
    
    
    1$response->assertStreamed();
    
    
    $response->assertStreamed();

#### assertStreamedContent

Assert that the given string matches the streamed response content:

```php $response->assertStreamedContent($value); ``` 

#### assertNotFound

Assert that the response has a not found (404) HTTP status code:

```php $response->assertNotFound(); ``` 

#### assertOk

Assert that the response has a 200 HTTP status code:

```php $response->assertOk(); ``` 

#### assertPaymentRequired

Assert that the response has a payment required (402) HTTP status code:

```php $response->assertPaymentRequired(); ``` 

#### assertPlainCookie

Assert that the response contains the given unencrypted cookie:

```php $response->assertPlainCookie($cookieName, $value = null); ``` 

#### assertRedirect

Assert that the response is a redirect to the given URI:

```php $response->assertRedirect($uri = null); ``` 

#### assertRedirectBack

Assert whether the response is redirecting back to the previous page:

```php $response->assertRedirectBack(); ``` 

#### assertRedirectBackWithErrors

Assert whether the response is redirecting back to the previous page and the session has the given errors:

```php $response->assertRedirectBackWithErrors( array $keys = [], $format = null, $errorBag = 'default' ); ``` 

#### assertRedirectBackWithoutErrors

Assert whether the response is redirecting back to the previous page and the session does not contain any error messages:

```php $response->assertRedirectBackWithoutErrors(); ``` 

#### assertRedirectContains

Assert whether the response is redirecting to a URI that contains the given string:

```php $response->assertRedirectContains($string); ``` 

#### assertRedirectToRoute

Assert that the response is a redirect to the given [named route](/docs/12.x/routing#named-routes):

```php $response->assertRedirectToRoute($name, $parameters = []); ``` 

#### assertRedirectToSignedRoute

Assert that the response is a redirect to the given [signed route](/docs/12.x/urls#signed-urls):

```php $response->assertRedirectToSignedRoute($name = null, $parameters = []); ``` 

#### assertRequestTimeout

Assert that the response has a request timeout (408) HTTP status code:

```php $response->assertRequestTimeout(); ``` 

#### assertSee

Assert that the given string is contained within the response. This assertion will automatically escape the given string unless you pass a second argument of `false`:

```php $response->assertSee($value, $escape = true); ``` 

#### assertSeeInOrder

Assert that the given strings are contained in order within the response. This assertion will automatically escape the given strings unless you pass a second argument of `false`:

```php $response->assertSeeInOrder(array $values, $escape = true); ``` 

#### assertSeeText

Assert that the given string is contained within the response text. This assertion will automatically escape the given string unless you pass a second argument of `false`. The response content will be passed to the `strip_tags` PHP function before the assertion is made:

```php $response->assertSeeText($value, $escape = true); ``` 

#### assertSeeTextInOrder

Assert that the given strings are contained in order within the response text. This assertion will automatically escape the given strings unless you pass a second argument of `false`. The response content will be passed to the `strip_tags` PHP function before the assertion is made:

```php $response->assertSeeTextInOrder(array $values, $escape = true); ``` 

#### assertServerError

Assert that the response has a server error (>= 500 , < 600) HTTP status code:

```php $response->assertServerError(); ``` 

#### assertServiceUnavailable

Assert that the response has a "Service Unavailable" (503) HTTP status code:

```php $response->assertServiceUnavailable(); ``` 

#### assertSessionHas

Assert that the session contains the given piece of data:

```php $response->assertSessionHas($key, $value = null); ``` 

If needed, a closure can be provided as the second argument to the `assertSessionHas` method. The assertion will pass if the closure returns `true`:

```php $response->assertSessionHas($key, function (User $value) { return $value->name === 'Taylor Otwell'; }); ``` 

#### assertSessionHasInput

Assert that the session has a given value in the [flashed input array](/docs/12.x/responses#redirecting-with-flashed-session-data):

```php $response->assertSessionHasInput($key, $value = null); ``` 

If needed, a closure can be provided as the second argument to the `assertSessionHasInput` method. The assertion will pass if the closure returns `true`:

```php use Illuminate\Support\Facades\Crypt; $response->assertSessionHasInput($key, function (string $value) { return Crypt::decryptString($value) === 'secret'; }); ``` 

#### assertSessionHasAll

Assert that the session contains a given array of key / value pairs:

```php $response->assertSessionHasAll(array $data); ``` 

For example, if your application's session contains `name` and `status` keys, you may assert that both exist and have the specified values like so:

```php $response->assertSessionHasAll([ 'name' => 'Taylor Otwell', 'status' => 'active', ]); ``` 

#### assertSessionHasErrors

Assert that the session contains an error for the given `$keys`. If `$keys` is an associative array, assert that the session contains a specific error message (value) for each field (key). This method should be used when testing routes that flash validation errors to the session instead of returning them as a JSON structure:

```php $response->assertSessionHasErrors( array $keys = [], $format = null, $errorBag = 'default' ); ``` 

For example, to assert that the `name` and `email` fields have validation error messages that were flashed to the session, you may invoke the `assertSessionHasErrors` method like so:

```php $response->assertSessionHasErrors(['name', 'email']); ``` 

Or, you may assert that a given field has a particular validation error message:

```php $response->assertSessionHasErrors([ 'name' => 'The given name was invalid.' ]); ``` 

The more generic assertInvalid method may be used to assert that a response has validation errors returned as JSON **or** that errors were flashed to session storage.

#### assertSessionHasErrorsIn

Assert that the session contains an error for the given `$keys` within a specific [error bag](/docs/12.x/validation#named-error-bags). If `$keys` is an associative array, assert that the session contains a specific error message (value) for each field (key), within the error bag:

```php $response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null); ``` 

#### assertSessionHasNoErrors

Assert that the session has no validation errors:

```php $response->assertSessionHasNoErrors(); ``` 

#### assertSessionDoesntHaveErrors

Assert that the session has no validation errors for the given keys:

```php $response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default'); ``` 

The more generic assertValid method may be used to assert that a response does not have validation errors that were returned as JSON **and** that no errors were flashed to session storage.

#### assertSessionMissing

Assert that the session does not contain the given key:

```php $response->assertSessionMissing($key); ``` 

#### assertStatus

Assert that the response has a given HTTP status code:

```php $response->assertStatus($code); ``` 

#### assertSuccessful

Assert that the response has a successful (>= 200 and < 300) HTTP status code:

```php $response->assertSuccessful(); ``` 

#### assertTooManyRequests

Assert that the response has a too many requests (429) HTTP status code:

```php $response->assertTooManyRequests(); ``` 

#### assertUnauthorized

Assert that the response has an unauthorized (401) HTTP status code:

```php $response->assertUnauthorized(); ``` 

#### assertUnprocessable

Assert that the response has an unprocessable entity (422) HTTP status code:

```php $response->assertUnprocessable(); ``` 

#### assertUnsupportedMediaType

Assert that the response has an unsupported media type (415) HTTP status code:

```php $response->assertUnsupportedMediaType(); ``` 

#### assertValid

Assert that the response has no validation errors for the given keys. This method may be used for asserting against responses where the validation errors are returned as a JSON structure or where the validation errors have been flashed to the session:

```php // Assert that no validation errors are present... $response->assertValid(); // Assert that the given keys do not have validation errors... $response->assertValid(['name', 'email']); ``` 

#### assertInvalid

Assert that the response has validation errors for the given keys. This method may be used for asserting against responses where the validation errors are returned as a JSON structure or where the validation errors have been flashed to the session:

```php $response->assertInvalid(['name', 'email']); ``` 

You may also assert that a given key has a particular validation error message. When doing so, you may provide the entire message or only a small portion of the message:

```php $response->assertInvalid([ 'name' => 'The name field is required.', 'email' => 'valid email address', ]); ``` 

If you would like to assert that the given fields are the only fields with validation errors, you may use the `assertOnlyInvalid` method:

```php $response->assertOnlyInvalid(['name', 'email']); ``` 

#### assertViewHas

Assert that the response view contains a given piece of data:

```php $response->assertViewHas($key, $value = null); ``` 

Passing a closure as the second argument to the `assertViewHas` method will allow you to inspect and make assertions against a particular piece of view data:

```php $response->assertViewHas('user', function (User $user) { return $user->name === 'Taylor'; }); ``` 

In addition, view data may be accessed as array variables on the response, allowing you to conveniently inspect it:

Pest PHPUnit

```php expect($response['name'])->toBe('Taylor'); ``` ```php $this->assertEquals('Taylor', $response['name']); ``` 

#### assertViewHasAll

Assert that the response view has a given list of data:

```php $response->assertViewHasAll(array $data); ``` 

This method may be used to assert that the view simply contains data matching the given keys:

```php $response->assertViewHasAll([ 'name', 'email', ]); ``` 

Or, you may assert that the view data is present and has specific values:

```php $response->assertViewHasAll([ 'name' => 'Taylor Otwell', 'email' => '[email protected],', ]); ``` 

#### assertViewIs

Assert that the given view was returned by the route:

```php $response->assertViewIs($value); ``` 

#### assertViewMissing

Assert that the given data key was not made available to the view returned in the application's response:

```php $response->assertViewMissing($key); ``` 

### Authentication Assertions

Laravel also provides a variety of authentication related assertions that you may utilize within your application's feature tests. Note that these methods are invoked on the test class itself and not the `Illuminate\Testing\TestResponse` instance returned by methods such as `get` and `post`.

#### assertAuthenticated

Assert that a user is authenticated:

```php $this->assertAuthenticated($guard = null); ``` 

#### assertGuest

Assert that a user is not authenticated:

```php $this->assertGuest($guard = null); ``` 

#### assertAuthenticatedAs

Assert that a specific user is authenticated:

```php $this->assertAuthenticatedAs($user, $guard = null); ``` 

## Validation Assertions

Laravel provides two primary validation related assertions that you may use to ensure the data provided in your request was either valid or invalid.

#### assertValid

Assert that the response has no validation errors for the given keys. This method may be used for asserting against responses where the validation errors are returned as a JSON structure or where the validation errors have been flashed to the session:

```php // Assert that no validation errors are present... $response->assertValid(); // Assert that the given keys do not have validation errors... $response->assertValid(['name', 'email']); ``` 

#### assertInvalid

Assert that the response has validation errors for the given keys. This method may be used for asserting against responses where the validation errors are returned as a JSON structure or where the validation errors have been flashed to the session:

```php $response->assertInvalid(['name', 'email']); ``` 

You may also assert that a given key has a particular validation error message. When doing so, you may provide the entire message or only a small portion of the message:

```php $response->assertInvalid([ 'name' => 'The name field is required.', 'email' => 'valid email address', ]); ``` 
