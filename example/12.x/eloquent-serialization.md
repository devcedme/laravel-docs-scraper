# Source: https://laravel.com/docs/12.x/eloquent-serialization

# Eloquent: Serialization

  * Introduction
  * Serializing Models and Collections
    * Serializing to Arrays
    * Serializing to JSON
  * Hiding Attributes From JSON
  * Appending Values to JSON
  * Date Serialization



## Introduction

When building APIs using Laravel, you will often need to convert your models and relationships to arrays or JSON. Eloquent includes convenient methods for making these conversions, as well as controlling which attributes are included in the serialized representation of your models.

For an even more robust way of handling Eloquent model and collection JSON serialization, check out the documentation on [Eloquent API resources](/docs/12.x/eloquent-resources).

## Serializing Models and Collections

### Serializing to Arrays

To convert a model and its loaded [relationships](/docs/12.x/eloquent-relationships) to an array, you should use the `toArray` method. This method is recursive, so all attributes and all relations (including the relations of relations) will be converted to arrays:

```php use App\Models\User; $user = User::with('roles')->first(); return $user->toArray(); ``` 

The `attributesToArray` method may be used to convert a model's attributes to an array but not its relationships:

```php $user = User::first(); return $user->attributesToArray(); ``` 

You may also convert entire [collections](/docs/12.x/eloquent-collections) of models to arrays by calling the `toArray` method on the collection instance:

```php $users = User::all(); return $users->toArray(); ``` 

### Serializing to JSON

To convert a model to JSON, you should use the `toJson` method. Like `toArray`, the `toJson` method is recursive, so all attributes and relations will be converted to JSON. You may also specify any JSON encoding options that are [supported by PHP](https://secure.php.net/manual/en/function.json-encode.php):

```php use App\Models\User; $user = User::find(1); return $user->toJson(); return $user->toJson(JSON_PRETTY_PRINT); ``` 

Alternatively, you may cast a model or collection to a string, which will automatically call the `toJson` method on the model or collection:

```php return (string) User::find(1); ``` 

Since models and collections are converted to JSON when cast to a string, you can return Eloquent objects directly from your application's routes or controllers. Laravel will automatically serialize your Eloquent models and collections to JSON when they are returned from routes or controllers:

```php Route::get('/users', function () { return User::all(); }); ``` 

#### Relationships

When an Eloquent model is converted to JSON, its loaded relationships will automatically be included as attributes on the JSON object. Also, though Eloquent relationship methods are defined using "camel case" method names, a relationship's JSON attribute will be "snake case".

## Hiding Attributes From JSON

Sometimes you may wish to limit the attributes, such as passwords, that are included in your model's array or JSON representation. To do so, add a `$hidden` property to your model. Attributes that are listed in the `$hidden` property's array will not be included in the serialized representation of your model:

```php <?php namespace App\Models; use Illuminate\Database\Eloquent\Model; class User extends Model { /** * The attributes that should be hidden for serialization. * * @var array<string> */ protected $hidden = ['password']; } ``` 

To hide relationships, add the relationship's method name to your Eloquent model's `$hidden` property.

Alternatively, you may use the `visible` property to define an "allow list" of attributes that should be included in your model's array and JSON representation. All attributes that are not present in the `$visible` array will be hidden when the model is converted to an array or JSON:

```php <?php namespace App\Models; use Illuminate\Database\Eloquent\Model; class User extends Model { /** * The attributes that should be visible in arrays. * * @var array */ protected $visible = ['first_name', 'last_name']; } ``` 

#### Temporarily Modifying Attribute Visibility

If you would like to make some typically hidden attributes visible on a given model instance, you may use the `makeVisible` method. The `makeVisible` method returns the model instance:

```php return $user->makeVisible('attribute')->toArray(); ``` 

Likewise, if you would like to hide some attributes that are typically visible, you may use the `makeHidden` method.

```php return $user->makeHidden('attribute')->toArray(); ``` 

If you wish to temporarily override all of the visible or hidden attributes, you may use the `setVisible` and `setHidden` methods respectively:

```php return $user->setVisible(['id', 'name'])->toArray(); return $user->setHidden(['email', 'password', 'remember_token'])->toArray(); ``` 

## Appending Values to JSON

Occasionally, when converting models to arrays or JSON, you may wish to add attributes that do not have a corresponding column in your database. To do so, first define an [accessor](/docs/12.x/eloquent-mutators) for the value:

```php <?php namespace App\Models; use Illuminate\Database\Eloquent\Casts\Attribute; use Illuminate\Database\Eloquent\Model; class User extends Model { /** * Determine if the user is an administrator. */ protected function isAdmin(): Attribute { return new Attribute( get: fn () => 'yes', ); } } ``` 

If you would like the accessor to always be appended to your model's array and JSON representations, you may add the attribute name to the `appends` property of your model. Note that attribute names are typically referenced using their "snake case" serialized representation, even though the accessor's PHP method is defined using "camel case":

```php <?php namespace App\Models; use Illuminate\Database\Eloquent\Model; class User extends Model { /** * The accessors to append to the model's array form. * * @var array */ protected $appends = ['is_admin']; } ``` 

Once the attribute has been added to the `appends` list, it will be included in both the model's array and JSON representations. Attributes in the `appends` array will also respect the `visible` and `hidden` settings configured on the model.

#### Appending at Run Time

At runtime, you may instruct a model instance to append additional attributes using the `append` method. Or, you may use the `setAppends` method to override the entire array of appended properties for a given model instance:

```php return $user->append('is_admin')->toArray(); return $user->setAppends(['is_admin'])->toArray(); ``` 

## Date Serialization

#### Customizing the Default Date Format

You may customize the default serialization format by overriding the `serializeDate` method. This method does not affect how your dates are formatted for storage in the database:

```php /** * Prepare a date for array / JSON serialization. */ protected function serializeDate(DateTimeInterface $date): string { return $date->format('Y-m-d'); } ``` 

#### Customizing the Date Format per Attribute

You may customize the serialization format of individual Eloquent date attributes by specifying the date format in the model's [cast declarations](/docs/12.x/eloquent-mutators#attribute-casting):

```php protected function casts(): array { return [ 'birthday' => 'date:Y-m-d', 'joined_at' => 'datetime:Y-m-d H:00', ]; } ``` 
