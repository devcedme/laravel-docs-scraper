# Source: https://laravel.com/docs/12.x/validation

# Validation

  * Introduction
  * Validation Quickstart
    * Defining the Routes
    * Creating the Controller
    * Writing the Validation Logic
    * Displaying the Validation Errors
    * Repopulating Forms
    * A Note on Optional Fields
    * Validation Error Response Format
  * Form Request Validation
    * Creating Form Requests
    * Authorizing Form Requests
    * Customizing the Error Messages
    * Preparing Input for Validation
  * Manually Creating Validators
    * Automatic Redirection
    * Named Error Bags
    * Customizing the Error Messages
    * Performing Additional Validation
  * Working With Validated Input
  * Working With Error Messages
    * Specifying Custom Messages in Language Files
    * Specifying Attributes in Language Files
    * Specifying Values in Language Files
  * Available Validation Rules
  * Conditionally Adding Rules
  * Validating Arrays
    * Validating Nested Array Input
    * Error Message Indexes and Positions
  * Validating Files
  * Validating Passwords
  * Custom Validation Rules
    * Using Rule Objects
    * Using Closures
    * Implicit Rules



## Introduction

Laravel provides several different approaches to validate your application's incoming data. It is most common to use the `validate` method available on all incoming HTTP requests. However, we will discuss other approaches to validation as well.

Laravel includes a wide variety of convenient validation rules that you may apply to data, even providing the ability to validate if values are unique in a given database table. We'll cover each of these validation rules in detail so that you are familiar with all of Laravel's validation features.

## Validation Quickstart

To learn about Laravel's powerful validation features, let's look at a complete example of validating a form and displaying the error messages back to the user. By reading this high-level overview, you'll be able to gain a good general understanding of how to validate incoming request data using Laravel:

### Defining the Routes

First, let's assume we have the following routes defined in our `routes/web.php` file:

```php use App\Http\Controllers\PostController; Route::get('/post/create', [PostController::class, 'create']); Route::post('/post', [PostController::class, 'store']); ``` 

The `GET` route will display a form for the user to create a new blog post, while the `POST` route will store the new blog post in the database.

### Creating the Controller

Next, let's take a look at a simple controller that handles incoming requests to these routes. We'll leave the `store` method empty for now:

```php <?php namespace App\Http\Controllers; use Illuminate\Http\RedirectResponse; use Illuminate\Http\Request; use Illuminate\View\View; class PostController extends Controller { /** * Show the form to create a new blog post. */ public function create(): View { return view('post.create'); } /** * Store a new blog post. */ public function store(Request $request): RedirectResponse { // Validate and store the blog post... $post = /** ... */ return to_route('post.show', ['post' => $post->id]); } } ``` 

### Writing the Validation Logic

Now we are ready to fill in our `store` method with the logic to validate the new blog post. To do this, we will use the `validate` method provided by the `Illuminate\Http\Request` object. If the validation rules pass, your code will keep executing normally; however, if validation fails, an `Illuminate\Validation\ValidationException` exception will be thrown and the proper error response will automatically be sent back to the user.

If validation fails during a traditional HTTP request, a redirect response to the previous URL will be generated. If the incoming request is an XHR request, a JSON response containing the validation error messages will be returned.

To get a better understanding of the `validate` method, let's jump back into the `store` method:

```php /** * Store a new blog post. */ public function store(Request $request): RedirectResponse { $validated = $request->validate([ 'title' => 'required|unique:posts|max:255', 'body' => 'required', ]); // The blog post is valid... return redirect('/posts'); } ``` 

As you can see, the validation rules are passed into the `validate` method. Don't worry - all available validation rules are documented. Again, if the validation fails, the proper response will automatically be generated. If the validation passes, our controller will continue executing normally.

Alternatively, validation rules may be specified as arrays of rules instead of a single `|` delimited string:

```php $validatedData = $request->validate([ 'title' => ['required', 'unique:posts', 'max:255'], 'body' => ['required'], ]); ``` 

In addition, you may use the `validateWithBag` method to validate a request and store any error messages within a named error bag:

```php $validatedData = $request->validateWithBag('post', [ 'title' => ['required', 'unique:posts', 'max:255'], 'body' => ['required'], ]); ``` 

#### Stopping on First Validation Failure

Sometimes you may wish to stop running validation rules on an attribute after the first validation failure. To do so, assign the `bail` rule to the attribute:

```php $request->validate([ 'title' => 'bail|required|unique:posts|max:255', 'body' => 'required', ]); ``` 

In this example, if the `unique` rule on the `title` attribute fails, the `max` rule will not be checked. Rules will be validated in the order they are assigned.

#### A Note on Nested Attributes

If the incoming HTTP request contains "nested" field data, you may specify these fields in your validation rules using "dot" syntax:

```php $request->validate([ 'title' => 'required|unique:posts|max:255', 'author.name' => 'required', 'author.description' => 'required', ]); ``` 

On the other hand, if your field name contains a literal period, you can explicitly prevent this from being interpreted as "dot" syntax by escaping the period with a backslash:

```php $request->validate([ 'title' => 'required|unique:posts|max:255', 'v1\\.0' => 'required', ]); ``` 

### Displaying the Validation Errors

So, what if the incoming request fields do not pass the given validation rules? As mentioned previously, Laravel will automatically redirect the user back to their previous location. In addition, all of the validation errors and [request input](/docs/12.x/requests#retrieving-old-input) will automatically be [flashed to the session](/docs/12.x/session#flash-data).

An `$errors` variable is shared with all of your application's views by the `Illuminate\View\Middleware\ShareErrorsFromSession` middleware, which is provided by the `web` middleware group. When this middleware is applied an `$errors` variable will always be available in your views, allowing you to conveniently assume the `$errors` variable is always defined and can be safely used. The `$errors` variable will be an instance of `Illuminate\Support\MessageBag`. For more information on working with this object, check out its documentation.

So, in our example, the user will be redirected to our controller's `create` method when validation fails, allowing us to display the error messages in the view:

```blade <!-- /resources/views/post/create.blade.php --> <h1>Create Post</h1> @if ($errors->any()) <div class="alert alert-danger"> <ul> @foreach ($errors->all() as $error) <li>{{ $error }}</li> @endforeach </ul> </div> @endif <!-- Create Post Form --> ``` 

#### Customizing the Error Messages

Laravel's built-in validation rules each have an error message that is located in your application's `lang/en/validation.php` file. If your application does not have a `lang` directory, you may instruct Laravel to create it using the `lang:publish` Artisan command.

Within the `lang/en/validation.php` file, you will find a translation entry for each validation rule. You are free to change or modify these messages based on the needs of your application.

In addition, you may copy this file to another language directory to translate the messages for your application's language. To learn more about Laravel localization, check out the complete [localization documentation](/docs/12.x/localization).

By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files, you may publish them via the `lang:publish` Artisan command.

#### XHR Requests and Validation

In this example, we used a traditional form to send data to the application. However, many applications receive XHR requests from a JavaScript powered frontend. When using the `validate` method during an XHR request, Laravel will not generate a redirect response. Instead, Laravel generates a JSON response containing all of the validation errors. This JSON response will be sent with a 422 HTTP status code.

#### The `@error` Directive

You may use the `@error` [Blade](/docs/12.x/blade) directive to quickly determine if validation error messages exist for a given attribute. Within an `@error` directive, you may echo the `$message` variable to display the error message:

```blade <!-- /resources/views/post/create.blade.php --> <label for="title">Post Title</label> <input id="title" type="text" name="title" class="@error('title') is-invalid @enderror" /> @error('title') <div class="alert alert-danger">{{ $message }}</div> @enderror ``` 

If you are using named error bags, you may pass the name of the error bag as the second argument to the `@error` directive:

```blade <input ... class="@error('title', 'post') is-invalid @enderror"> ``` 

### Repopulating Forms

When Laravel generates a redirect response due to a validation error, the framework will automatically [flash all of the request's input to the session](/docs/12.x/session#flash-data). This is done so that you may conveniently access the input during the next request and repopulate the form that the user attempted to submit.

To retrieve flashed input from the previous request, invoke the `old` method on an instance of `Illuminate\Http\Request`. The `old` method will pull the previously flashed input data from the [session](/docs/12.x/session):

```php $title = $request->old('title'); ``` 

Laravel also provides a global `old` helper. If you are displaying old input within a [Blade template](/docs/12.x/blade), it is more convenient to use the `old` helper to repopulate the form. If no old input exists for the given field, `null` will be returned:

```blade <input type="text" name="title" value="{{ old('title') }}"> ``` 

### A Note on Optional Fields

By default, Laravel includes the `TrimStrings` and `ConvertEmptyStringsToNull` middleware in your application's global middleware stack. Because of this, you will often need to mark your "optional" request fields as `nullable` if you do not want the validator to consider `null` values as invalid. For example:

```php $request->validate([ 'title' => 'required|unique:posts|max:255', 'body' => 'required', 'publish_at' => 'nullable|date', ]); ``` 

In this example, we are specifying that the `publish_at` field may be either `null` or a valid date representation. If the `nullable` modifier is not added to the rule definition, the validator would consider `null` an invalid date.

### Validation Error Response Format

When your application throws a `Illuminate\Validation\ValidationException` exception and the incoming HTTP request is expecting a JSON response, Laravel will automatically format the error messages for you and return a `422 Unprocessable Entity` HTTP response.

Below, you can review an example of the JSON response format for validation errors. Note that nested error keys are flattened into "dot" notation format:

```json { "message": "The team name must be a string. (and 4 more errors)", "errors": { "team_name": [ "The team name must be a string.", "The team name must be at least 1 characters." ], "authorization.role": [ "The selected authorization.role is invalid." ], "users.0.email": [ "The users.0.email field is required." ], "users.2.email": [ "The users.2.email must be a valid email address." ] } } ``` 

## Form Request Validation

### Creating Form Requests

For more complex validation scenarios, you may wish to create a "form request". Form requests are custom request classes that encapsulate their own validation and authorization logic. To create a form request class, you may use the `make:request` Artisan CLI command:

```shell php artisan make:request StorePostRequest ``` 

The generated form request class will be placed in the `app/Http/Requests` directory. If this directory does not exist, it will be created when you run the `make:request` command. Each form request generated by Laravel has two methods: `authorize` and `rules`.

As you might have guessed, the `authorize` method is responsible for determining if the currently authenticated user can perform the action represented by the request, while the `rules` method returns the validation rules that should apply to the request's data:

```php /** * Get the validation rules that apply to the request. * * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string> */ public function rules(): array { return [ 'title' => 'required|unique:posts|max:255', 'body' => 'required', ]; } ``` 

You may type-hint any dependencies you require within the `rules` method's signature. They will automatically be resolved via the Laravel [service container](/docs/12.x/container).

So, how are the validation rules evaluated? All you need to do is type-hint the request on your controller method. The incoming form request is validated before the controller method is called, meaning you do not need to clutter your controller with any validation logic:

```php /** * Store a new blog post. */ public function store(StorePostRequest $request): RedirectResponse { // The incoming request is valid... // Retrieve the validated input data... $validated = $request->validated(); // Retrieve a portion of the validated input data... $validated = $request->safe()->only(['name', 'email']); $validated = $request->safe()->except(['name', 'email']); // Store the blog post... return redirect('/posts'); } ``` 

If validation fails, a redirect response will be generated to send the user back to their previous location. The errors will also be flashed to the session so they are available for display. If the request was an XHR request, an HTTP response with a 422 status code will be returned to the user including a JSON representation of the validation errors.

Need to add real-time form request validation to your Inertia powered Laravel frontend? Check out [Laravel Precognition](/docs/12.x/precognition).

#### Performing Additional Validation

Sometimes you need to perform additional validation after your initial validation is complete. You can accomplish this using the form request's `after` method.

The `after` method should return an array of callables or closures which will be invoked after validation is complete. The given callables will receive an `Illuminate\Validation\Validator` instance, allowing you to raise additional error messages if necessary:

```php use Illuminate\Validation\Validator; /** * Get the "after" validation callables for the request. */ public function after(): array { return [ function (Validator $validator) { if ($this->somethingElseIsInvalid()) { $validator->errors()->add( 'field', 'Something is wrong with this field!' ); } } ]; } ``` 

As noted, the array returned by the `after` method may also contain invokable classes. The `__invoke` method of these classes will receive an `Illuminate\Validation\Validator` instance:

```php use App\Validation\ValidateShippingTime; use App\Validation\ValidateUserStatus; use Illuminate\Validation\Validator; /** * Get the "after" validation callables for the request. */ public function after(): array { return [ new ValidateUserStatus, new ValidateShippingTime, function (Validator $validator) { // } ]; } ``` 

#### Stopping on the First Validation Failure

By adding a `stopOnFirstFailure` property to your request class, you may inform the validator that it should stop validating all attributes once a single validation failure has occurred:

```php /** * Indicates if the validator should stop on the first rule failure. * * @var bool */ protected $stopOnFirstFailure = true; ``` 

#### Customizing the Redirect Location

When form request validation fails, a redirect response will be generated to send the user back to their previous location. However, you are free to customize this behavior. To do so, define a `$redirect` property on your form request:

```php /** * The URI that users should be redirected to if validation fails. * * @var string */ protected $redirect = '/dashboard'; ``` 

Or, if you would like to redirect users to a named route, you may define a `$redirectRoute` property instead:

```php /** * The route that users should be redirected to if validation fails. * * @var string */ protected $redirectRoute = 'dashboard'; ``` 

### Authorizing Form Requests

The form request class also contains an `authorize` method. Within this method, you may determine if the authenticated user actually has the authority to update a given resource. For example, you may determine if a user actually owns a blog comment they are attempting to update. Most likely, you will interact with your [authorization gates and policies](/docs/12.x/authorization) within this method:

```php use App\Models\Comment; /** * Determine if the user is authorized to make this request. */ public function authorize(): bool { $comment = Comment::find($this->route('comment')); return $comment && $this->user()->can('update', $comment); } ``` 

Since all form requests extend the base Laravel request class, we may use the `user` method to access the currently authenticated user. Also, note the call to the `route` method in the example above. This method grants you access to the URI parameters defined on the route being called, such as the `{comment}` parameter in the example below:

```php Route::post('/comment/{comment}'); ``` 

Therefore, if your application is taking advantage of [route model binding](/docs/12.x/routing#route-model-binding), your code may be made even more succinct by accessing the resolved model as a property of the request:

```php return $this->user()->can('update', $this->comment); ``` 

If the `authorize` method returns `false`, an HTTP response with a 403 status code will automatically be returned and your controller method will not execute.

If you plan to handle authorization logic for the request in another part of your application, you may remove the `authorize` method completely, or simply return `true`:

```php /** * Determine if the user is authorized to make this request. */ public function authorize(): bool { return true; } ``` 

You may type-hint any dependencies you need within the `authorize` method's signature. They will automatically be resolved via the Laravel [service container](/docs/12.x/container).

### Customizing the Error Messages

You may customize the error messages used by the form request by overriding the `messages` method. This method should return an array of attribute / rule pairs and their corresponding error messages:

```php /** * Get the error messages for the defined validation rules. * * @return array<string, string> */ public function messages(): array { return [ 'title.required' => 'A title is required', 'body.required' => 'A message is required', ]; } ``` 

#### Customizing the Validation Attributes

Many of Laravel's built-in validation rule error messages contain an `:attribute` placeholder. If you would like the `:attribute` placeholder of your validation message to be replaced with a custom attribute name, you may specify the custom names by overriding the `attributes` method. This method should return an array of attribute / name pairs:

```php /** * Get custom attributes for validator errors. * * @return array<string, string> */ public function attributes(): array { return [ 'email' => 'email address', ]; } ``` 

### Preparing Input for Validation

If you need to prepare or sanitize any data from the request before you apply your validation rules, you may use the `prepareForValidation` method:

```php use Illuminate\Support\Str; /** * Prepare the data for validation. */ protected function prepareForValidation(): void { $this->merge([ 'slug' => Str::slug($this->slug), ]); } ``` 

Likewise, if you need to normalize any request data after validation is complete, you may use the `passedValidation` method:

```php /** * Handle a passed validation attempt. */ protected function passedValidation(): void { $this->replace(['name' => 'Taylor']); } ``` 

## Manually Creating Validators

If you do not want to use the `validate` method on the request, you may create a validator instance manually using the `Validator` [facade](/docs/12.x/facades). The `make` method on the facade generates a new validator instance:

```php <?php namespace App\Http\Controllers; use Illuminate\Http\RedirectResponse; use Illuminate\Http\Request; use Illuminate\Support\Facades\Validator; class PostController extends Controller { /** * Store a new blog post. */ public function store(Request $request): RedirectResponse { $validator = Validator::make($request->all(), [ 'title' => 'required|unique:posts|max:255', 'body' => 'required', ]); if ($validator->fails()) { return redirect('/post/create') ->withErrors($validator) ->withInput(); } // Retrieve the validated input... $validated = $validator->validated(); // Retrieve a portion of the validated input... $validated = $validator->safe()->only(['name', 'email']); $validated = $validator->safe()->except(['name', 'email']); // Store the blog post... return redirect('/posts'); } } ``` 

The first argument passed to the `make` method is the data under validation. The second argument is an array of the validation rules that should be applied to the data.

After determining whether the request validation failed, you may use the `withErrors` method to flash the error messages to the session. When using this method, the `$errors` variable will automatically be shared with your views after redirection, allowing you to easily display them back to the user. The `withErrors` method accepts a validator, a `MessageBag`, or a PHP `array`.

#### Stopping on First Validation Failure

The `stopOnFirstFailure` method will inform the validator that it should stop validating all attributes once a single validation failure has occurred:

```php if ($validator->stopOnFirstFailure()->fails()) { // ... } ``` 

### Automatic Redirection

If you would like to create a validator instance manually but still take advantage of the automatic redirection offered by the HTTP request's `validate` method, you may call the `validate` method on an existing validator instance. If validation fails, the user will automatically be redirected or, in the case of an XHR request, a JSON response will be returned:

```php Validator::make($request->all(), [ 'title' => 'required|unique:posts|max:255', 'body' => 'required', ])->validate(); ``` 

You may use the `validateWithBag` method to store the error messages in a named error bag if validation fails:

```php Validator::make($request->all(), [ 'title' => 'required|unique:posts|max:255', 'body' => 'required', ])->validateWithBag('post'); ``` 

### Named Error Bags

If you have multiple forms on a single page, you may wish to name the `MessageBag` containing the validation errors, allowing you to retrieve the error messages for a specific form. To achieve this, pass a name as the second argument to `withErrors`:

```php return redirect('/register')->withErrors($validator, 'login'); ``` 

You may then access the named `MessageBag` instance from the `$errors` variable:

```blade {{ $errors->login->first('email') }} ``` 

### Customizing the Error Messages

If needed, you may provide custom error messages that a validator instance should use instead of the default error messages provided by Laravel. There are several ways to specify custom messages. First, you may pass the custom messages as the third argument to the `Validator::make` method:

```php $validator = Validator::make($input, $rules, $messages = [ 'required' => 'The :attribute field is required.', ]); ``` 

In this example, the `:attribute` placeholder will be replaced by the actual name of the field under validation. You may also utilize other placeholders in validation messages. For example:

```php $messages = [ 'same' => 'The :attribute and :other must match.', 'size' => 'The :attribute must be exactly :size.', 'between' => 'The :attribute value :input is not between :min - :max.', 'in' => 'The :attribute must be one of the following types: :values', ]; ``` 

#### Specifying a Custom Message for a Given Attribute

Sometimes you may wish to specify a custom error message only for a specific attribute. You may do so using "dot" notation. Specify the attribute's name first, followed by the rule:

```php $messages = [ 'email.required' => 'We need to know your email address!', ]; ``` 

#### Specifying Custom Attribute Values

Many of Laravel's built-in error messages include an `:attribute` placeholder that is replaced with the name of the field or attribute under validation. To customize the values used to replace these placeholders for specific fields, you may pass an array of custom attributes as the fourth argument to the `Validator::make` method:

```php $validator = Validator::make($input, $rules, $messages, [ 'email' => 'email address', ]); ``` 

### Performing Additional Validation

Sometimes you need to perform additional validation after your initial validation is complete. You can accomplish this using the validator's `after` method. The `after` method accepts a closure or an array of callables which will be invoked after validation is complete. The given callables will receive an `Illuminate\Validation\Validator` instance, allowing you to raise additional error messages if necessary:

```php use Illuminate\Support\Facades\Validator; $validator = Validator::make(/* ... */); $validator->after(function ($validator) { if ($this->somethingElseIsInvalid()) { $validator->errors()->add( 'field', 'Something is wrong with this field!' ); } }); if ($validator->fails()) { // ... } ``` 

As noted, the `after` method also accepts an array of callables, which is particularly convenient if your "after validation" logic is encapsulated in invokable classes, which will receive an `Illuminate\Validation\Validator` instance via their `__invoke` method:

```php use App\Validation\ValidateShippingTime; use App\Validation\ValidateUserStatus; $validator->after([ new ValidateUserStatus, new ValidateShippingTime, function ($validator) { // ... }, ]); ``` 

## Working With Validated Input

After validating incoming request data using a form request or a manually created validator instance, you may wish to retrieve the incoming request data that actually underwent validation. This can be accomplished in several ways. First, you may call the `validated` method on a form request or validator instance. This method returns an array of the data that was validated:

```php $validated = $request->validated(); $validated = $validator->validated(); ``` 

Alternatively, you may call the `safe` method on a form request or validator instance. This method returns an instance of `Illuminate\Support\ValidatedInput`. This object exposes `only`, `except`, and `all` methods to retrieve a subset of the validated data or the entire array of validated data:

```php $validated = $request->safe()->only(['name', 'email']); $validated = $request->safe()->except(['name', 'email']); $validated = $request->safe()->all(); ``` 

In addition, the `Illuminate\Support\ValidatedInput` instance may be iterated over and accessed like an array:

```php // Validated data may be iterated... foreach ($request->safe() as $key => $value) { // ... } // Validated data may be accessed as an array... $validated = $request->safe(); $email = $validated['email']; ``` 

If you would like to add additional fields to the validated data, you may call the `merge` method:

```php $validated = $request->safe()->merge(['name' => 'Taylor Otwell']); ``` 

If you would like to retrieve the validated data as a [collection](/docs/12.x/collections) instance, you may call the `collect` method:

```php $collection = $request->safe()->collect(); ``` 

## Working With Error Messages

After calling the `errors` method on a `Validator` instance, you will receive an `Illuminate\Support\MessageBag` instance, which has a variety of convenient methods for working with error messages. The `$errors` variable that is automatically made available to all views is also an instance of the `MessageBag` class.

#### Retrieving the First Error Message for a Field

To retrieve the first error message for a given field, use the `first` method:

```php $errors = $validator->errors(); echo $errors->first('email'); ``` 

#### Retrieving All Error Messages for a Field

If you need to retrieve an array of all the messages for a given field, use the `get` method:

```php foreach ($errors->get('email') as $message) { // ... } ``` 

If you are validating an array form field, you may retrieve all of the messages for each of the array elements using the `*` character:

```php foreach ($errors->get('attachments.*') as $message) { // ... } ``` 

#### Retrieving All Error Messages for All Fields

To retrieve an array of all messages for all fields, use the `all` method:

```php foreach ($errors->all() as $message) { // ... } ``` 

#### Determining if Messages Exist for a Field

The `has` method may be used to determine if any error messages exist for a given field:

```php if ($errors->has('email')) { // ... } ``` 

### Specifying Custom Messages in Language Files

Laravel's built-in validation rules each have an error message that is located in your application's `lang/en/validation.php` file. If your application does not have a `lang` directory, you may instruct Laravel to create it using the `lang:publish` Artisan command.

Within the `lang/en/validation.php` file, you will find a translation entry for each validation rule. You are free to change or modify these messages based on the needs of your application.

In addition, you may copy this file to another language directory to translate the messages for your application's language. To learn more about Laravel localization, check out the complete [localization documentation](/docs/12.x/localization).

By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files, you may publish them via the `lang:publish` Artisan command.

#### Custom Messages for Specific Attributes

You may customize the error messages used for specified attribute and rule combinations within your application's validation language files. To do so, add your message customizations to the `custom` array of your application's `lang/xx/validation.php` language file:

```php 'custom' => [ 'email' => [ 'required' => 'We need to know your email address!', 'max' => 'Your email address is too long!' ], ], ``` 

### Specifying Attributes in Language Files

Many of Laravel's built-in error messages include an `:attribute` placeholder that is replaced with the name of the field or attribute under validation. If you would like the `:attribute` portion of your validation message to be replaced with a custom value, you may specify the custom attribute name in the `attributes` array of your `lang/xx/validation.php` language file:

```php 'attributes' => [ 'email' => 'email address', ], ``` 

By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files, you may publish them via the `lang:publish` Artisan command.

### Specifying Values in Language Files

Some of Laravel's built-in validation rule error messages contain a `:value` placeholder that is replaced with the current value of the request attribute. However, you may occasionally need the `:value` portion of your validation message to be replaced with a custom representation of the value. For example, consider the following rule that specifies that a credit card number is required if the `payment_type` has a value of `cc`:

```php Validator::make($request->all(), [ 'credit_card_number' => 'required_if:payment_type,cc' ]); ``` 

If this validation rule fails, it will produce the following error message:

```text The credit card number field is required when payment type is cc. ``` 

Instead of displaying `cc` as the payment type value, you may specify a more user-friendly value representation in your `lang/xx/validation.php` language file by defining a `values` array:

```php 'values' => [ 'payment_type' => [ 'cc' => 'credit card' ], ], ``` 

By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files, you may publish them via the `lang:publish` Artisan command.

After defining this value, the validation rule will produce the following error message:

```text The credit card number field is required when payment type is credit card. ``` 

## Available Validation Rules

Below is a list of all available validation rules and their function:

#### Booleans

Accepted Accepted If Boolean Declined Declined If

#### Strings

Active URL Alpha Alpha Dash Alpha Numeric Ascii Confirmed Current Password Different Doesnt Start With Doesnt End With Email Ends With Enum Hex Color In IP Address JSON Lowercase MAC Address Max Min Not In Regular Expression Not Regular Expression Same Size Starts With String Uppercase URL ULID UUID

#### Numbers

Between Decimal Different Digits Digits Between Greater Than Greater Than Or Equal Integer Less Than Less Than Or Equal Max Max Digits Min Min Digits Multiple Of Numeric Same Size

#### Arrays

Array Between Contains Distinct In Array In Array Keys List Max Min Size

#### Dates

After After Or Equal Before Before Or Equal Date Date Equals Date Format Different Timezone

#### Files

Between Dimensions Extensions File Image Max MIME Types MIME Type By File Extension Size

#### Database

Exists Unique

#### Utilities

Any Of Bail Exclude Exclude If Exclude Unless Exclude With Exclude Without Filled Missing Missing If Missing Unless Missing With Missing With All Nullable Present Present If Present Unless Present With Present With All Prohibited Prohibited If Prohibited If Accepted Prohibited If Declined Prohibited Unless Prohibits Required Required If Required If Accepted Required If Declined Required Unless Required With Required With All Required Without Required Without All Required Array Keys Sometimes

#### accepted

The field under validation must be `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"`. This is useful for validating "Terms of Service" acceptance or similar fields.

#### accepted_if:anotherfield,value,...

The field under validation must be `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"` if another field under validation is equal to a specified value. This is useful for validating "Terms of Service" acceptance or similar fields.

#### active_url

The field under validation must have a valid A or AAAA record according to the `dns_get_record` PHP function. The hostname of the provided URL is extracted using the `parse_url` PHP function before being passed to `dns_get_record`.

#### after:_date_

The field under validation must be a value after a given date. The dates will be passed into the `strtotime` PHP function in order to be converted to a valid `DateTime` instance:

```php 'start_date' => 'required|date|after:tomorrow' ``` 

Instead of passing a date string to be evaluated by `strtotime`, you may specify another field to compare against the date:

```php 'finish_date' => 'required|date|after:start_date' ``` 

For convenience, date-based rules may be constructed using the fluent `date` rule builder:

```php use Illuminate\Validation\Rule; 'start_date' => [ 'required', Rule::date()->after(today()->addDays(7)), ], ``` 

The `afterToday` and `todayOrAfter` methods may be used to fluently express the date must be after today or or today or after, respectively:

```php 'start_date' => [ 'required', Rule::date()->afterToday(), ], ``` 

#### after_or_equal:_date_

The field under validation must be a value after or equal to the given date. For more information, see the after rule.

For convenience, date-based rules may be constructed using the fluent `date` rule builder:

```php use Illuminate\Validation\Rule; 'start_date' => [ 'required', Rule::date()->afterOrEqual(today()->addDays(7)), ], ``` 

#### anyOf

The `Rule::anyOf` validation rule allows you to specify that the field under validation must satisfy any of the given validation rulesets. For example, the following rule will validate that the `username` field is either an email address or an alpha-numeric string (including dashes) that is at least 6 characters long:

```php use Illuminate\Validation\Rule; 'username' => [ 'required', Rule::anyOf([ ['string', 'email'], ['string', 'alpha_dash', 'min:6'], ]), ], ``` 

#### alpha

The field under validation must be entirely Unicode alphabetic characters contained in [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) and [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=).

To restrict this validation rule to characters in the ASCII range (`a-z` and `A-Z`), you may provide the `ascii` option to the validation rule:

```php 'username' => 'alpha:ascii', ``` 

#### alpha_dash

The field under validation must be entirely Unicode alpha-numeric characters contained in [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=), as well as ASCII dashes (`-`) and ASCII underscores (`_`).

To restrict this validation rule to characters in the ASCII range (`a-z`, `A-Z`, and `0-9`), you may provide the `ascii` option to the validation rule:

```php 'username' => 'alpha_dash:ascii', ``` 

#### alpha_num

The field under validation must be entirely Unicode alpha-numeric characters contained in [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), and [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=).

To restrict this validation rule to characters in the ASCII range (`a-z`, `A-Z`, and `0-9`), you may provide the `ascii` option to the validation rule:

```php 'username' => 'alpha_num:ascii', ``` 

#### array

The field under validation must be a PHP `array`.

When additional values are provided to the `array` rule, each key in the input array must be present within the list of values provided to the rule. In the following example, the `admin` key in the input array is invalid since it is not contained in the list of values provided to the `array` rule:

```php use Illuminate\Support\Facades\Validator; $input = [ 'user' => [ 'name' => 'Taylor Otwell', 'username' => 'taylorotwell', 'admin' => true, ], ]; Validator::make($input, [ 'user' => 'array:name,username', ]); ``` 

In general, you should always specify the array keys that are allowed to be present within your array.

#### ascii

The field under validation must be entirely 7-bit ASCII characters.

#### bail

Stop running validation rules for the field after the first validation failure.

While the `bail` rule will only stop validating a specific field when it encounters a validation failure, the `stopOnFirstFailure` method will inform the validator that it should stop validating all attributes once a single validation failure has occurred:

```php if ($validator->stopOnFirstFailure()->fails()) { // ... } ``` 

#### before:_date_

The field under validation must be a value preceding the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. In addition, like the after rule, the name of another field under validation may be supplied as the value of `date`.

For convenience, date-based rules may also be constructed using the fluent `date` rule builder:

```php use Illuminate\Validation\Rule; 'start_date' => [ 'required', Rule::date()->before(today()->subDays(7)), ], ``` 

The `beforeToday` and `todayOrBefore` methods may be used to fluently express the date must be before today or or today or before, respectively:

```php 'start_date' => [ 'required', Rule::date()->beforeToday(), ], ``` 

#### before_or_equal:_date_

The field under validation must be a value preceding or equal to the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. In addition, like the after rule, the name of another field under validation may be supplied as the value of `date`.

For convenience, date-based rules may also be constructed using the fluent `date` rule builder:

```php use Illuminate\Validation\Rule; 'start_date' => [ 'required', Rule::date()->beforeOrEqual(today()->subDays(7)), ], ``` 

#### between:_min_ ,_max_

The field under validation must have a size between the given _min_ and _max_ (inclusive). Strings, numerics, arrays, and files are evaluated in the same fashion as the size rule.

#### boolean

The field under validation must be able to be cast as a boolean. Accepted input are `true`, `false`, `1`, `0`, `"1"`, and `"0"`.

#### confirmed

The field under validation must have a matching field of `{field}_confirmation`. For example, if the field under validation is `password`, a matching `password_confirmation` field must be present in the input.

You may also pass a custom confirmation field name. For example, `confirmed:repeat_username` will expect the field `repeat_username` to match the field under validation.

#### contains:_foo_ ,_bar_ ,...

The field under validation must be an array that contains all of the given parameter values. Since this rule often requires you to `implode` an array, the `Rule::contains` method may be used to fluently construct the rule:

```php use Illuminate\Support\Facades\Validator; use Illuminate\Validation\Rule; Validator::make($data, [ 'roles' => [ 'required', 'array', Rule::contains(['admin', 'editor']), ], ]); ``` 

#### current_password

The field under validation must match the authenticated user's password. You may specify an [authentication guard](/docs/12.x/authentication) using the rule's first parameter:

```php 'password' => 'current_password:api' ``` 

#### date

The field under validation must be a valid, non-relative date according to the `strtotime` PHP function.

#### date_equals:_date_

The field under validation must be equal to the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance.

#### date_format:_format_ ,...

The field under validation must match one of the given _formats_. You should use **either** `date` or `date_format` when validating a field, not both. This validation rule supports all formats supported by PHP's [DateTime](https://www.php.net/manual/en/class.datetime.php) class.

For convenience, date-based rules may be constructed using the fluent `date` rule builder:

```php use Illuminate\Validation\Rule; 'start_date' => [ 'required', Rule::date()->format('Y-m-d'), ], ``` 

#### decimal:_min_ ,_max_

The field under validation must be numeric and must contain the specified number of decimal places:

```php // Must have exactly two decimal places (9.99)... 'price' => 'decimal:2' // Must have between 2 and 4 decimal places... 'price' => 'decimal:2,4' ``` 

#### declined

The field under validation must be `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"`.

#### declined_if:anotherfield,value,...

The field under validation must be `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"` if another field under validation is equal to a specified value.

#### different:_field_

The field under validation must have a different value than _field_.

#### digits:_value_

The integer under validation must have an exact length of _value_.

#### digits_between:_min_ ,_max_

The integer validation must have a length between the given _min_ and _max_.

#### dimensions

The file under validation must be an image meeting the dimension constraints as specified by the rule's parameters:

```php 'avatar' => 'dimensions:min_width=100,min_height=200' ``` 

Available constraints are: _min_width_ , _max_width_ , _min_height_ , _max_height_ , _width_ , _height_ , _ratio_.

A _ratio_ constraint should be represented as width divided by height. This can be specified either by a fraction like `3/2` or a float like `1.5`:

```php 'avatar' => 'dimensions:ratio=3/2' ``` 

Since this rule requires several arguments, it is often more convenient to use the `Rule::dimensions` method to fluently construct the rule:

```php use Illuminate\Support\Facades\Validator; use Illuminate\Validation\Rule; Validator::make($data, [ 'avatar' => [ 'required', Rule::dimensions() ->maxWidth(1000) ->maxHeight(500) ->ratio(3 / 2), ], ]); ``` 

#### distinct

When validating arrays, the field under validation must not have any duplicate values:

```php 'foo.*.id' => 'distinct' ``` 

Distinct uses loose variable comparisons by default. To use strict comparisons, you may add the `strict` parameter to your validation rule definition:

```php 'foo.*.id' => 'distinct:strict' ``` 

You may add `ignore_case` to the validation rule's arguments to make the rule ignore capitalization differences:

```php 'foo.*.id' => 'distinct:ignore_case' ``` 

#### doesnt_start_with:_foo_ ,_bar_ ,...

The field under validation must not start with one of the given values.

#### doesnt_end_with:_foo_ ,_bar_ ,...

The field under validation must not end with one of the given values.

#### email

The field under validation must be formatted as an email address. This validation rule utilizes the [egulias/email-validator](https://github.com/egulias/EmailValidator) package for validating the email address. By default, the `RFCValidation` validator is applied, but you can apply other validation styles as well:

```php 'email' => 'email:rfc,dns' ``` 

The example above will apply the `RFCValidation` and `DNSCheckValidation` validations. Here's a full list of validation styles you can apply:

  * `rfc`: `RFCValidation` \- Validate the email address according to [supported RFCs](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs).
  * `strict`: `NoRFCWarningsValidation` \- Validate the email according to [supported RFCs](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs), failing when warnings are found (e.g. trailing periods and multiple consecutive periods).
  * `dns`: `DNSCheckValidation` \- Ensure the email address's domain has a valid MX record.
  * `spoof`: `SpoofCheckValidation` \- Ensure the email address does not contain homograph or deceptive Unicode characters.
  * `filter`: `FilterEmailValidation` \- Ensure the email address is valid according to PHP's `filter_var` function.
  * `filter_unicode`: `FilterEmailValidation::unicode()` \- Ensure the email address is valid according to PHP's `filter_var` function, allowing some Unicode characters.



For convenience, email validation rules may be built using the fluent rule builder:

```php use Illuminate\Validation\Rule; $request->validate([ 'email' => [ 'required', Rule::email() ->rfcCompliant(strict: false) ->validateMxRecord() ->preventSpoofing() ], ]); ``` 

The `dns` and `spoof` validators require the PHP `intl` extension.

#### ends_with:_foo_ ,_bar_ ,...

The field under validation must end with one of the given values.

#### enum

The `Enum` rule is a class-based rule that validates whether the field under validation contains a valid enum value. The `Enum` rule accepts the name of the enum as its only constructor argument. When validating primitive values, a backed Enum should be provided to the `Enum` rule:

```php use App\Enums\ServerStatus; use Illuminate\Validation\Rule; $request->validate([ 'status' => [Rule::enum(ServerStatus::class)], ]); ``` 

The `Enum` rule's `only` and `except` methods may be used to limit which enum cases should be considered valid:

```php Rule::enum(ServerStatus::class) ->only([ServerStatus::Pending, ServerStatus::Active]); Rule::enum(ServerStatus::class) ->except([ServerStatus::Pending, ServerStatus::Active]); ``` 

The `when` method may be used to conditionally modify the `Enum` rule:

```php use Illuminate\Support\Facades\Auth; use Illuminate\Validation\Rule; Rule::enum(ServerStatus::class) ->when( Auth::user()->isAdmin(), fn ($rule) => $rule->only(...), fn ($rule) => $rule->only(...), ); ``` 

#### exclude

The field under validation will be excluded from the request data returned by the `validate` and `validated` methods.

#### exclude_if:_anotherfield_ ,_value_

The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is equal to _value_.

If complex conditional exclusion logic is required, you may utilize the `Rule::excludeIf` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should be excluded:

```php use Illuminate\Support\Facades\Validator; use Illuminate\Validation\Rule; Validator::make($request->all(), [ 'role_id' => Rule::excludeIf($request->user()->is_admin), ]); Validator::make($request->all(), [ 'role_id' => Rule::excludeIf(fn () => $request->user()->is_admin), ]); ``` 

#### exclude_unless:_anotherfield_ ,_value_

The field under validation will be excluded from the request data returned by the `validate` and `validated` methods unless _anotherfield_ 's field is equal to _value_. If _value_ is `null` (`exclude_unless:name,null`), the field under validation will be excluded unless the comparison field is `null` or the comparison field is missing from the request data.

#### exclude_with:_anotherfield_

The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is present.

#### exclude_without:_anotherfield_

The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is not present.

#### exists:_table_ ,_column_

The field under validation must exist in a given database table.

#### Basic Usage of Exists Rule

```php 'state' => 'exists:states' ``` 

If the `column` option is not specified, the field name will be used. So, in this case, the rule will validate that the `states` database table contains a record with a `state` column value matching the request's `state` attribute value.

#### Specifying a Custom Column Name

You may explicitly specify the database column name that should be used by the validation rule by placing it after the database table name:

```php 'state' => 'exists:states,abbreviation' ``` 

Occasionally, you may need to specify a specific database connection to be used for the `exists` query. You can accomplish this by prepending the connection name to the table name:

```php 'email' => 'exists:connection.staff,email' ``` 

Instead of specifying the table name directly, you may specify the Eloquent model which should be used to determine the table name:

```php 'user_id' => 'exists:App\Models\User,id' ``` 

If you would like to customize the query executed by the validation rule, you may use the `Rule` class to fluently define the rule. In this example, we'll also specify the validation rules as an array instead of using the `|` character to delimit them:

```php use Illuminate\Database\Query\Builder; use Illuminate\Support\Facades\Validator; use Illuminate\Validation\Rule; Validator::make($data, [ 'email' => [ 'required', Rule::exists('staff')->where(function (Builder $query) { $query->where('account_id', 1); }), ], ]); ``` 

You may explicitly specify the database column name that should be used by the `exists` rule generated by the `Rule::exists` method by providing the column name as the second argument to the `exists` method:

```php 'state' => Rule::exists('states', 'abbreviation'), ``` 

Sometimes, you may wish to validate whether an array of values exists in the database. You can do so by adding both the `exists` and array rules to the field being validated:

```php 'states' => ['array', Rule::exists('states', 'abbreviation')], ``` 

When both of these rules are assigned to a field, Laravel will automatically build a single query to determine if all of the given values exist in the specified table.

#### extensions:_foo_ ,_bar_ ,...

The file under validation must have a user-assigned extension corresponding to one of the listed extensions:

```php 'photo' => ['required', 'extensions:jpg,png'], ``` 

You should never rely on validating a file by its user-assigned extension alone. This rule should typically always be used in combination with the mimes or mimetypes rules.

#### file

The field under validation must be a successfully uploaded file.

#### filled

The field under validation must not be empty when it is present.

#### gt:_field_

The field under validation must be greater than the given _field_ or _value_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the size rule.

#### gte:_field_

The field under validation must be greater than or equal to the given _field_ or _value_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the size rule.

#### hex_color

The field under validation must contain a valid color value in [hexadecimal](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) format.

#### image

The file under validation must be an image (jpg, jpeg, png, bmp, gif, or webp).

By default, the image rule does not allow SVG files due to the possibility of XSS vulnerabilities. If you need to allow SVG files, you may provide the `allow_svg` directive to the `image` rule (`image:allow_svg`).

#### in:_foo_ ,_bar_ ,...

The field under validation must be included in the given list of values. Since this rule often requires you to `implode` an array, the `Rule::in` method may be used to fluently construct the rule:

```php use Illuminate\Support\Facades\Validator; use Illuminate\Validation\Rule; Validator::make($data, [ 'zones' => [ 'required', Rule::in(['first-zone', 'second-zone']), ], ]); ``` 

When the `in` rule is combined with the `array` rule, each value in the input array must be present within the list of values provided to the `in` rule. In the following example, the `LAS` airport code in the input array is invalid since it is not contained in the list of airports provided to the `in` rule:

```php use Illuminate\Support\Facades\Validator; use Illuminate\Validation\Rule; $input = [ 'airports' => ['NYC', 'LAS'], ]; Validator::make($input, [ 'airports' => [ 'required', 'array', ], 'airports.*' => Rule::in(['NYC', 'LIT']), ]); ``` 

#### in_array:_anotherfield_.*

The field under validation must exist in _anotherfield_ 's values.

#### in_array_keys:_value_.*

The field under validation must be an array having at least one of the given _values_ as a key within the array:

```php 'config' => 'array|in_array_keys:timezone' ``` 

#### integer

The field under validation must be an integer.

This validation rule does not verify that the input is of the "integer" variable type, only that the input is of a type accepted by PHP's `FILTER_VALIDATE_INT` rule. If you need to validate the input as being a number please use this rule in combination with the `numeric` validation rule.

#### ip

The field under validation must be an IP address.

#### ipv4

The field under validation must be an IPv4 address.

#### ipv6

The field under validation must be an IPv6 address.

#### json

The field under validation must be a valid JSON string.

#### lt:_field_

The field under validation must be less than the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the size rule.

#### lte:_field_

The field under validation must be less than or equal to the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the size rule.

#### lowercase

The field under validation must be lowercase.

#### list

The field under validation must be an array that is a list. An array is considered a list if its keys consist of consecutive numbers from 0 to `count($array) - 1`.

#### mac_address

The field under validation must be a MAC address.

#### max:_value_

The field under validation must be less than or equal to a maximum _value_. Strings, numerics, arrays, and files are evaluated in the same fashion as the size rule.

#### max_digits:_value_

The integer under validation must have a maximum length of _value_.

#### mimetypes:_text/plain_ ,...

The file under validation must match one of the given MIME types:

```php 'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime' ``` 

To determine the MIME type of the uploaded file, the file's contents will be read and the framework will attempt to guess the MIME type, which may be different from the client's provided MIME type.

#### mimes:_foo_ ,_bar_ ,...

The file under validation must have a MIME type corresponding to one of the listed extensions:

```php 'photo' => 'mimes:jpg,bmp,png' ``` 

Even though you only need to specify the extensions, this rule actually validates the MIME type of the file by reading the file's contents and guessing its MIME type. A full listing of MIME types and their corresponding extensions may be found at the following location:

<https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types>

#### MIME Types and Extensions

This validation rule does not verify agreement between the MIME type and the extension the user assigned to the file. For example, the `mimes:png` validation rule would consider a file containing valid PNG content to be a valid PNG image, even if the file is named `photo.txt`. If you would like to validate the user-assigned extension of the file, you may use the extensions rule.

#### min:_value_

The field under validation must have a minimum _value_. Strings, numerics, arrays, and files are evaluated in the same fashion as the size rule.

#### min_digits:_value_

The integer under validation must have a minimum length of _value_.

#### multiple_of:_value_

The field under validation must be a multiple of _value_.

#### missing

The field under validation must not be present in the input data.

#### missing_if:_anotherfield_ ,_value_ ,...

The field under validation must not be present if the _anotherfield_ field is equal to any _value_.

#### missing_unless:_anotherfield_ ,_value_

The field under validation must not be present unless the _anotherfield_ field is equal to any _value_.

#### missing_with:_foo_ ,_bar_ ,...

The field under validation must not be present _only if_ any of the other specified fields are present.

#### missing_with_all:_foo_ ,_bar_ ,...

The field under validation must not be present _only if_ all of the other specified fields are present.

#### not_in:_foo_ ,_bar_ ,...

The field under validation must not be included in the given list of values. The `Rule::notIn` method may be used to fluently construct the rule:

```php use Illuminate\Validation\Rule; Validator::make($data, [ 'toppings' => [ 'required', Rule::notIn(['sprinkles', 'cherries']), ], ]); ``` 

#### not_regex:_pattern_

The field under validation must not match the given regular expression.

Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => 'not_regex:/^.+$/i'`.

When using the `regex` / `not_regex` patterns, it may be necessary to specify your validation rules using an array instead of using `|` delimiters, especially if the regular expression contains a `|` character.

#### nullable

The field under validation may be `null`.

#### numeric

The field under validation must be [numeric](https://www.php.net/manual/en/function.is-numeric.php).

#### present

The field under validation must exist in the input data.

#### present_if:_anotherfield_ ,_value_ ,...

The field under validation must be present if the _anotherfield_ field is equal to any _value_.

#### present_unless:_anotherfield_ ,_value_

The field under validation must be present unless the _anotherfield_ field is equal to any _value_.

#### present_with:_foo_ ,_bar_ ,...

The field under validation must be present _only if_ any of the other specified fields are present.

#### present_with_all:_foo_ ,_bar_ ,...

The field under validation must be present _only if_ all of the other specified fields are present.

#### prohibited

The field under validation must be missing or empty. A field is "empty" if it meets one of the following criteria:

  * The value is `null`.
  * The value is an empty string.
  * The value is an empty array or empty `Countable` object.
  * The value is an uploaded file with an empty path.



#### prohibited_if:_anotherfield_ ,_value_ ,...

The field under validation must be missing or empty if the _anotherfield_ field is equal to any _value_. A field is "empty" if it meets one of the following criteria:

  * The value is `null`.
  * The value is an empty string.
  * The value is an empty array or empty `Countable` object.
  * The value is an uploaded file with an empty path.



If complex conditional prohibition logic is required, you may utilize the `Rule::prohibitedIf` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should be prohibited:

```php use Illuminate\Support\Facades\Validator; use Illuminate\Validation\Rule; Validator::make($request->all(), [ 'role_id' => Rule::prohibitedIf($request->user()->is_admin), ]); Validator::make($request->all(), [ 'role_id' => Rule::prohibitedIf(fn () => $request->user()->is_admin), ]); ``` 

#### prohibited_if_accepted:_anotherfield_ ,...

The field under validation must be missing or empty if the _anotherfield_ field is equal to `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"`.

#### prohibited_if_declined:_anotherfield_ ,...

The field under validation must be missing or empty if the _anotherfield_ field is equal to `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"`.

#### prohibited_unless:_anotherfield_ ,_value_ ,...

The field under validation must be missing or empty unless the _anotherfield_ field is equal to any _value_. A field is "empty" if it meets one of the following criteria:

  * The value is `null`.
  * The value is an empty string.
  * The value is an empty array or empty `Countable` object.
  * The value is an uploaded file with an empty path.



#### prohibits:_anotherfield_ ,...

If the field under validation is not missing or empty, all fields in _anotherfield_ must be missing or empty. A field is "empty" if it meets one of the following criteria:

  * The value is `null`.
  * The value is an empty string.
  * The value is an empty array or empty `Countable` object.
  * The value is an uploaded file with an empty path.



#### regex:_pattern_

The field under validation must match the given regular expression.

Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => 'regex:/^.+@.+$/i'`.

When using the `regex` / `not_regex` patterns, it may be necessary to specify rules in an array instead of using `|` delimiters, especially if the regular expression contains a `|` character.

#### required

The field under validation must be present in the input data and not empty. A field is "empty" if it meets one of the following criteria:

  * The value is `null`.
  * The value is an empty string.
  * The value is an empty array or empty `Countable` object.
  * The value is an uploaded file with no path.



#### required_if:_anotherfield_ ,_value_ ,...

The field under validation must be present and not empty if the _anotherfield_ field is equal to any _value_.

If you would like to construct a more complex condition for the `required_if` rule, you may use the `Rule::requiredIf` method. This method accepts a boolean or a closure. When passed a closure, the closure should return `true` or `false` to indicate if the field under validation is required:

```php use Illuminate\Support\Facades\Validator; use Illuminate\Validation\Rule; Validator::make($request->all(), [ 'role_id' => Rule::requiredIf($request->user()->is_admin), ]); Validator::make($request->all(), [ 'role_id' => Rule::requiredIf(fn () => $request->user()->is_admin), ]); ``` 

#### required_if_accepted:_anotherfield_ ,...

The field under validation must be present and not empty if the _anotherfield_ field is equal to `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"`.

#### required_if_declined:_anotherfield_ ,...

The field under validation must be present and not empty if the _anotherfield_ field is equal to `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"`.

#### required_unless:_anotherfield_ ,_value_ ,...

The field under validation must be present and not empty unless the _anotherfield_ field is equal to any _value_. This also means _anotherfield_ must be present in the request data unless _value_ is `null`. If _value_ is `null` (`required_unless:name,null`), the field under validation will be required unless the comparison field is `null` or the comparison field is missing from the request data.

#### required_with:_foo_ ,_bar_ ,...

The field under validation must be present and not empty _only if_ any of the other specified fields are present and not empty.

#### required_with_all:_foo_ ,_bar_ ,...

The field under validation must be present and not empty _only if_ all of the other specified fields are present and not empty.

#### required_without:_foo_ ,_bar_ ,...

The field under validation must be present and not empty _only when_ any of the other specified fields are empty or not present.

#### required_without_all:_foo_ ,_bar_ ,...

The field under validation must be present and not empty _only when_ all of the other specified fields are empty or not present.

#### required_array_keys:_foo_ ,_bar_ ,...

The field under validation must be an array and must contain at least the specified keys.

#### same:_field_

The given _field_ must match the field under validation.

#### size:_value_

The field under validation must have a size matching the given _value_. For string data, _value_ corresponds to the number of characters. For numeric data, _value_ corresponds to a given integer value (the attribute must also have the `numeric` or `integer` rule). For an array, _size_ corresponds to the `count` of the array. For files, _size_ corresponds to the file size in kilobytes. Let's look at some examples:

```php // Validate that a string is exactly 12 characters long... 'title' => 'size:12'; // Validate that a provided integer equals 10... 'seats' => 'integer|size:10'; // Validate that an array has exactly 5 elements... 'tags' => 'array|size:5'; // Validate that an uploaded file is exactly 512 kilobytes... 'image' => 'file|size:512'; ``` 

#### starts_with:_foo_ ,_bar_ ,...

The field under validation must start with one of the given values.

#### string

The field under validation must be a string. If you would like to allow the field to also be `null`, you should assign the `nullable` rule to the field.

#### timezone

The field under validation must be a valid timezone identifier according to the `DateTimeZone::listIdentifiers` method.

The arguments [accepted by the `DateTimeZone::listIdentifiers` method](https://www.php.net/manual/en/datetimezone.listidentifiers.php) may also be provided to this validation rule:

```php 'timezone' => 'required|timezone:all'; 'timezone' => 'required|timezone:Africa'; 'timezone' => 'required|timezone:per_country,US'; ``` 

#### unique:_table_ ,_column_

The field under validation must not exist within the given database table.

**Specifying a Custom Table / Column Name:**

Instead of specifying the table name directly, you may specify the Eloquent model which should be used to determine the table name:

```php 'email' => 'unique:App\Models\User,email_address' ``` 

The `column` option may be used to specify the field's corresponding database column. If the `column` option is not specified, the name of the field under validation will be used.

```php 'email' => 'unique:users,email_address' ``` 

**Specifying a Custom Database Connection**

Occasionally, you may need to set a custom connection for database queries made by the Validator. To accomplish this, you may prepend the connection name to the table name:

```php 'email' => 'unique:connection.users,email_address' ``` 

**Forcing a Unique Rule to Ignore a Given ID:**

Sometimes, you may wish to ignore a given ID during unique validation. For example, consider an "update profile" screen that includes the user's name, email address, and location. You will probably want to verify that the email address is unique. However, if the user only changes the name field and not the email field, you do not want a validation error to be thrown because the user is already the owner of the email address in question.

To instruct the validator to ignore the user's ID, we'll use the `Rule` class to fluently define the rule. In this example, we'll also specify the validation rules as an array instead of using the `|` character to delimit the rules:

```php use Illuminate\Support\Facades\Validator; use Illuminate\Validation\Rule; Validator::make($data, [ 'email' => [ 'required', Rule::unique('users')->ignore($user->id), ], ]); ``` 

You should never pass any user controlled request input into the `ignore` method. Instead, you should only pass a system generated unique ID such as an auto-incrementing ID or UUID from an Eloquent model instance. Otherwise, your application will be vulnerable to an SQL injection attack.

Instead of passing the model key's value to the `ignore` method, you may also pass the entire model instance. Laravel will automatically extract the key from the model:

```php Rule::unique('users')->ignore($user) ``` 

If your table uses a primary key column name other than `id`, you may specify the name of the column when calling the `ignore` method:

```php Rule::unique('users')->ignore($user->id, 'user_id') ``` 

By default, the `unique` rule will check the uniqueness of the column matching the name of the attribute being validated. However, you may pass a different column name as the second argument to the `unique` method:

```php Rule::unique('users', 'email_address')->ignore($user->id) ``` 

**Adding Additional Where Clauses:**

You may specify additional query conditions by customizing the query using the `where` method. For example, let's add a query condition that scopes the query to only search records that have an `account_id` column value of `1`:

```php 'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1)) ``` 

**Ignoring Soft Deleted Records in Unique Checks:**

By default, the unique rule includes soft deleted records when determining uniqueness. To exclude soft deleted records from the uniqueness check, you may invoke the `withoutTrashed` method:

```php Rule::unique('users')->withoutTrashed(); ``` 

If your model uses a column name other than `deleted_at` for soft deleted records, you may provide the column name when invoking the `withoutTrashed` method:

```php Rule::unique('users')->withoutTrashed('was_deleted_at'); ``` 

#### uppercase

The field under validation must be uppercase.

#### url

The field under validation must be a valid URL.

If you would like to specify the URL protocols that should be considered valid, you may pass the protocols as validation rule parameters:

```php 'url' => 'url:http,https', 'game' => 'url:minecraft,steam', ``` 

#### ulid

The field under validation must be a valid [Universally Unique Lexicographically Sortable Identifier](https://github.com/ulid/spec) (ULID).

#### uuid

The field under validation must be a valid RFC 9562 (version 1, 3, 4, 5, 6, 7, or 8) universally unique identifier (UUID).

You may also validate that the given UUID matches a UUID specification by version:

```php 'uuid' => 'uuid:4' ``` 

## Conditionally Adding Rules

#### Skipping Validation When Fields Have Certain Values

You may occasionally wish to not validate a given field if another field has a given value. You may accomplish this using the `exclude_if` validation rule. In this example, the `appointment_date` and `doctor_name` fields will not be validated if the `has_appointment` field has a value of `false`:

```php use Illuminate\Support\Facades\Validator; $validator = Validator::make($data, [ 'has_appointment' => 'required|boolean', 'appointment_date' => 'exclude_if:has_appointment,false|required|date', 'doctor_name' => 'exclude_if:has_appointment,false|required|string', ]); ``` 

Alternatively, you may use the `exclude_unless` rule to not validate a given field unless another field has a given value:

```php $validator = Validator::make($data, [ 'has_appointment' => 'required|boolean', 'appointment_date' => 'exclude_unless:has_appointment,true|required|date', 'doctor_name' => 'exclude_unless:has_appointment,true|required|string', ]); ``` 

#### Validating When Present

In some situations, you may wish to run validation checks against a field **only** if that field is present in the data being validated. To quickly accomplish this, add the `sometimes` rule to your rule list:

```php $validator = Validator::make($data, [ 'email' => 'sometimes|required|email', ]); ``` 

In the example above, the `email` field will only be validated if it is present in the `$data` array.

If you are attempting to validate a field that should always be present but may be empty, check out this note on optional fields.

#### Complex Conditional Validation

Sometimes you may wish to add validation rules based on more complex conditional logic. For example, you may wish to require a given field only if another field has a greater value than 100. Or, you may need two fields to have a given value only when another field is present. Adding these validation rules doesn't have to be a pain. First, create a `Validator` instance with your _static rules_ that never change:

```php use Illuminate\Support\Facades\Validator; $validator = Validator::make($request->all(), [ 'email' => 'required|email', 'games' => 'required|integer|min:0', ]); ``` 

Let's assume our web application is for game collectors. If a game collector registers with our application and they own more than 100 games, we want them to explain why they own so many games. For example, perhaps they run a game resale shop, or maybe they just enjoy collecting games. To conditionally add this requirement, we can use the `sometimes` method on the `Validator` instance.

```php use Illuminate\Support\Fluent; $validator->sometimes('reason', 'required|max:500', function (Fluent $input) { return $input->games >= 100; }); ``` 

The first argument passed to the `sometimes` method is the name of the field we are conditionally validating. The second argument is a list of the rules we want to add. If the closure passed as the third argument returns `true`, the rules will be added. This method makes it a breeze to build complex conditional validations. You may even add conditional validations for several fields at once:

```php $validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) { return $input->games >= 100; }); ``` 

The `$input` parameter passed to your closure will be an instance of `Illuminate\Support\Fluent` and may be used to access your input and files under validation.

#### Complex Conditional Array Validation

Sometimes you may want to validate a field based on another field in the same nested array whose index you do not know. In these situations, you may allow your closure to receive a second argument which will be the current individual item in the array being validated:

```php $input = [ 'channels' => [ [ 'type' => 'email', 'address' => '[email protected]', ], [ 'type' => 'url', 'address' => 'https://example.com', ], ], ]; $validator->sometimes('channels.*.address', 'email', function (Fluent $input, Fluent $item) { return $item->type === 'email'; }); $validator->sometimes('channels.*.address', 'url', function (Fluent $input, Fluent $item) { return $item->type !== 'email'; }); ``` 

Like the `$input` parameter passed to the closure, the `$item` parameter is an instance of `Illuminate\Support\Fluent` when the attribute data is an array; otherwise, it is a string.

## Validating Arrays

As discussed in the array validation rule documentation, the `array` rule accepts a list of allowed array keys. If any additional keys are present within the array, validation will fail:

```php use Illuminate\Support\Facades\Validator; $input = [ 'user' => [ 'name' => 'Taylor Otwell', 'username' => 'taylorotwell', 'admin' => true, ], ]; Validator::make($input, [ 'user' => 'array:name,username', ]); ``` 

In general, you should always specify the array keys that are allowed to be present within your array. Otherwise, the validator's `validate` and `validated` methods will return all of the validated data, including the array and all of its keys, even if those keys were not validated by other nested array validation rules.

### Validating Nested Array Input

Validating nested array based form input fields doesn't have to be a pain. You may use "dot notation" to validate attributes within an array. For example, if the incoming HTTP request contains a `photos[profile]` field, you may validate it like so:

```php use Illuminate\Support\Facades\Validator; $validator = Validator::make($request->all(), [ 'photos.profile' => 'required|image', ]); ``` 

You may also validate each element of an array. For example, to validate that each email in a given array input field is unique, you may do the following:

```php $validator = Validator::make($request->all(), [ 'person.*.email' => 'email|unique:users', 'person.*.first_name' => 'required_with:person.*.last_name', ]); ``` 

Likewise, you may use the `*` character when specifying custom validation messages in your language files, making it a breeze to use a single validation message for array based fields:

```php 'custom' => [ 'person.*.email' => [ 'unique' => 'Each person must have a unique email address', ] ], ``` 

#### Accessing Nested Array Data

Sometimes you may need to access the value for a given nested array element when assigning validation rules to the attribute. You may accomplish this using the `Rule::forEach` method. The `forEach` method accepts a closure that will be invoked for each iteration of the array attribute under validation and will receive the attribute's value and explicit, fully-expanded attribute name. The closure should return an array of rules to assign to the array element:

```php use App\Rules\HasPermission; use Illuminate\Support\Facades\Validator; use Illuminate\Validation\Rule; $validator = Validator::make($request->all(), [ 'companies.*.id' => Rule::forEach(function (string|null $value, string $attribute) { return [ Rule::exists(Company::class, 'id'), new HasPermission('manage-company', $value), ]; }), ]); ``` 

### Error Message Indexes and Positions

When validating arrays, you may want to reference the index or position of a particular item that failed validation within the error message displayed by your application. To accomplish this, you may include the `:index` (starts from `0`) and `:position` (starts from `1`) placeholders within your custom validation message:

```php use Illuminate\Support\Facades\Validator; $input = [ 'photos' => [ [ 'name' => 'BeachVacation.jpg', 'description' => 'A photo of my beach vacation!', ], [ 'name' => 'GrandCanyon.jpg', 'description' => '', ], ], ]; Validator::validate($input, [ 'photos.*.description' => 'required', ], [ 'photos.*.description.required' => 'Please describe photo #:position.', ]); ``` 

Given the example above, validation will fail and the user will be presented with the following error of _"Please describe photo #2."_

If necessary, you may reference more deeply nested indexes and positions via `second-index`, `second-position`, `third-index`, `third-position`, etc.

```php 'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.', ``` 

## Validating Files

Laravel provides a variety of validation rules that may be used to validate uploaded files, such as `mimes`, `image`, `min`, and `max`. While you are free to specify these rules individually when validating files, Laravel also offers a fluent file validation rule builder that you may find convenient:

```php use Illuminate\Support\Facades\Validator; use Illuminate\Validation\Rules\File; Validator::validate($input, [ 'attachment' => [ 'required', File::types(['mp3', 'wav']) ->min(1024) ->max(12 * 1024), ], ]); ``` 

#### Validating File Types

Even though you only need to specify the extensions when invoking the `types` method, this method actually validates the MIME type of the file by reading the file's contents and guessing its MIME type. A full listing of MIME types and their corresponding extensions may be found at the following location:

<https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types>

#### Validating File Sizes

For convenience, minimum and maximum file sizes may be specified as a string with a suffix indicating the file size units. The `kb`, `mb`, `gb`, and `tb` suffixes are supported:

```php File::types(['mp3', 'wav']) ->min('1kb') ->max('10mb'); ``` 

#### Validating Image Files

If your application accepts images uploaded by your users, you may use the `File` rule's `image` constructor method to ensure that the file under validation is an image (jpg, jpeg, png, bmp, gif, or webp).

In addition, the `dimensions` rule may be used to limit the dimensions of the image:

```php use Illuminate\Support\Facades\Validator; use Illuminate\Validation\Rule; use Illuminate\Validation\Rules\File; Validator::validate($input, [ 'photo' => [ 'required', File::image() ->min(1024) ->max(12 * 1024) ->dimensions(Rule::dimensions()->maxWidth(1000)->maxHeight(500)), ], ]); ``` 

More information regarding validating image dimensions may be found in the dimension rule documentation.

By default, the `image` rule does not allow SVG files due to the possibility of XSS vulnerabilities. If you need to allow SVG files, you may pass `allowSvg: true` to the `image` rule: `File::image(allowSvg: true)`.

#### Validating Image Dimensions

You may also validate the dimensions of an image. For example, to validate that an uploaded image is at least 1000 pixels wide and 500 pixels tall, you may use the `dimensions` rule:

```php use Illuminate\Validation\Rule; use Illuminate\Validation\Rules\File; File::image()->dimensions( Rule::dimensions() ->maxWidth(1000) ->maxHeight(500) ) ``` 

More information regarding validating image dimensions may be found in the dimension rule documentation.

## Validating Passwords

To ensure that passwords have an adequate level of complexity, you may use Laravel's `Password` rule object:

```php use Illuminate\Support\Facades\Validator; use Illuminate\Validation\Rules\Password; $validator = Validator::make($request->all(), [ 'password' => ['required', 'confirmed', Password::min(8)], ]); ``` 

The `Password` rule object allows you to easily customize the password complexity requirements for your application, such as specifying that passwords require at least one letter, number, symbol, or characters with mixed casing:

```php // Require at least 8 characters... Password::min(8) // Require at least one letter... Password::min(8)->letters() // Require at least one uppercase and one lowercase letter... Password::min(8)->mixedCase() // Require at least one number... Password::min(8)->numbers() // Require at least one symbol... Password::min(8)->symbols() ``` 

In addition, you may ensure that a password has not been compromised in a public password data breach leak using the `uncompromised` method:

```php Password::min(8)->uncompromised() ``` 

Internally, the `Password` rule object uses the [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) model to determine if a password has been leaked via the [haveibeenpwned.com](https://haveibeenpwned.com) service without sacrificing the user's privacy or security.

By default, if a password appears at least once in a data leak, it will be considered compromised. You can customize this threshold using the first argument of the `uncompromised` method:

```php // Ensure the password appears less than 3 times in the same data leak... Password::min(8)->uncompromised(3); ``` 

Of course, you may chain all the methods in the examples above:

```php Password::min(8) ->letters() ->mixedCase() ->numbers() ->symbols() ->uncompromised() ``` 

#### Defining Default Password Rules

You may find it convenient to specify the default validation rules for passwords in a single location of your application. You can easily accomplish this using the `Password::defaults` method, which accepts a closure. The closure given to the `defaults` method should return the default configuration of the Password rule. Typically, the `defaults` rule should be called within the `boot` method of one of your application's service providers:

```php use Illuminate\Validation\Rules\Password; /** * Bootstrap any application services. */ public function boot(): void { Password::defaults(function () { $rule = Password::min(8); return $this->app->isProduction() ? $rule->mixedCase()->uncompromised() : $rule; }); } ``` 

Then, when you would like to apply the default rules to a particular password undergoing validation, you may invoke the `defaults` method with no arguments:

```php 'password' => ['required', Password::defaults()], ``` 

Occasionally, you may want to attach additional validation rules to your default password validation rules. You may use the `rules` method to accomplish this:

```php use App\Rules\ZxcvbnRule; Password::defaults(function () { $rule = Password::min(8)->rules([new ZxcvbnRule]); // ... }); ``` 

## Custom Validation Rules

### Using Rule Objects

Laravel provides a variety of helpful validation rules; however, you may wish to specify some of your own. One method of registering custom validation rules is using rule objects. To generate a new rule object, you may use the `make:rule` Artisan command. Let's use this command to generate a rule that verifies a string is uppercase. Laravel will place the new rule in the `app/Rules` directory. If this directory does not exist, Laravel will create it when you execute the Artisan command to create your rule:

```shell php artisan make:rule Uppercase ``` 

Once the rule has been created, we are ready to define its behavior. A rule object contains a single method: `validate`. This method receives the attribute name, its value, and a callback that should be invoked on failure with the validation error message:

```php <?php namespace App\Rules; use Closure; use Illuminate\Contracts\Validation\ValidationRule; class Uppercase implements ValidationRule { /** * Run the validation rule. */ public function validate(string $attribute, mixed $value, Closure $fail): void { if (strtoupper($value) !== $value) { $fail('The :attribute must be uppercase.'); } } } ``` 

Once the rule has been defined, you may attach it to a validator by passing an instance of the rule object with your other validation rules:

```php use App\Rules\Uppercase; $request->validate([ 'name' => ['required', 'string', new Uppercase], ]); ``` 

#### Translating Validation Messages

Instead of providing a literal error message to the `$fail` closure, you may also provide a [translation string key](/docs/12.x/localization) and instruct Laravel to translate the error message:

```php if (strtoupper($value) !== $value) { $fail('validation.uppercase')->translate(); } ``` 

If necessary, you may provide placeholder replacements and the preferred language as the first and second arguments to the `translate` method:

```php $fail('validation.location')->translate([ 'value' => $this->value, ], 'fr'); ``` 

#### Accessing Additional Data

If your custom validation rule class needs to access all of the other data undergoing validation, your rule class may implement the `Illuminate\Contracts\Validation\DataAwareRule` interface. This interface requires your class to define a `setData` method. This method will automatically be invoked by Laravel (before validation proceeds) with all of the data under validation:

```php <?php namespace App\Rules; use Illuminate\Contracts\Validation\DataAwareRule; use Illuminate\Contracts\Validation\ValidationRule; class Uppercase implements DataAwareRule, ValidationRule { /** * All of the data under validation. * * @var array<string, mixed> */ protected $data = []; // ... /** * Set the data under validation. * * @param array<string, mixed> $data */ public function setData(array $data): static { $this->data = $data; return $this; } } ``` 

Or, if your validation rule requires access to the validator instance performing the validation, you may implement the `ValidatorAwareRule` interface:

```php <?php namespace App\Rules; use Illuminate\Contracts\Validation\ValidationRule; use Illuminate\Contracts\Validation\ValidatorAwareRule; use Illuminate\Validation\Validator; class Uppercase implements ValidationRule, ValidatorAwareRule { /** * The validator instance. * * @var \Illuminate\Validation\Validator */ protected $validator; // ... /** * Set the current validator. */ public function setValidator(Validator $validator): static { $this->validator = $validator; return $this; } } ``` 

### Using Closures

If you only need the functionality of a custom rule once throughout your application, you may use a closure instead of a rule object. The closure receives the attribute's name, the attribute's value, and a `$fail` callback that should be called if validation fails:

```php use Illuminate\Support\Facades\Validator; use Closure; $validator = Validator::make($request->all(), [ 'title' => [ 'required', 'max:255', function (string $attribute, mixed $value, Closure $fail) { if ($value === 'foo') { $fail("The {$attribute} is invalid."); } }, ], ]); ``` 

### Implicit Rules

By default, when an attribute being validated is not present or contains an empty string, normal validation rules, including custom rules, are not run. For example, the unique rule will not be run against an empty string:

```php use Illuminate\Support\Facades\Validator; $rules = ['name' => 'unique:users,name']; $input = ['name' => '']; Validator::make($input, $rules)->passes(); // true ``` 

For a custom rule to run even when an attribute is empty, the rule must imply that the attribute is required. To quickly generate a new implicit rule object, you may use the `make:rule` Artisan command with the `--implicit` option:

```shell php artisan make:rule Uppercase --implicit ``` 

An "implicit" rule only _implies_ that the attribute is required. Whether it actually invalidates a missing or empty attribute is up to you.
