"""
Serializers for recipe APIs
"""
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.models import Recipe, Tag, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""

    class Meta:
        model = Ingredient
        fields = ["id", "name"]
        read_only_fields = ["id"]


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


"""
PatchedRecipeDetail{

title	string
maxLength: 255

time_minutes	integer
maximum: 2147483647
minimum: -2147483648

price	string($decimal)
pattern: ^\d{0,3}(\.\d{0,2})?$
#
^: 匹配字符串的開始。
\d{0,3}: 匹配0到3位的數字。這意味著它可以匹配空字符串、一位數字、兩位數字或三位數字。
(\.\d{0,2})?: 這是一個可選的分組。
\.: 匹配小數點。
\d{0,2}: 匹配0到2位的數字。這意味著它可以匹配空字符串、一位數字或兩位數字。
?: 表示前面的分組是可選的，即可以有也可以沒有。
$: 匹配字符串的結束。

link	string
maxLength: 255

tags	[Tag{
name*	string
maxLength: 255
}]

description	string
}
"""


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    tags = TagSerializer(many=True, required=False)
    """
    tags：這是一個多對多字段，它使用 TagSerializer 來序列化標籤。
    many=True 表示該字段可以包含多個標籤。
    required=False 表示在創建或更新食譜時，此字段不是必需的。
    """
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "time_minutes",
            "price",
            "link",
            "tags",
            "ingredients",
        ]
        read_only_fields = ["id"]

    """
    fields: 列出要序列化/反序列化的模型字段。
    如模型中字段設定為 blank=True 時，對應的序列化器字段會自動被視為 required=False。
    read_only_fields: 定義哪些字段是只讀的。在這裡，id 字段被標記為只讀，因此它不會被反序列化。
    """

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""
        auth_user = self.context["request"].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            """
            _get_or_create_tags Method, “內部的”方法, 避免和get_or_create方法衝突
            user=auth_user: 這指定了要查找的 Tag 對象必須屬於當前的 auth_user。
            **tag: 這使用 Python 的解包語法將 tag 字典的鍵/值對傳遞為參數。
            例如，如果 tag 是 {"name": "Indian"}，則這相當於傳遞 name="Indian" 作為參數。
            tag_obj, created: get_or_create 方法返回兩個值。
            第一個是找到或創建的對象，第二個是一個布爾值，指示是否創建了新對象。
            如果找到了對象，則 created 為 False；
            如果創建了新對象，則為 True。
            """
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        """Handle getting or creating ingredients as needed."""
        auth_user = self.context["request"].user
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop("tags", [])
        ingredients = validated_data.pop("ingredients", [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        request = self.context["request"]

        # 檢查 PUT 請求是否包含所有必需的字段
        if request.method == "PUT":
            required_fields = [
                f.name
                for f in Recipe._meta.fields
                if not (f.blank is True or f.null is True) and f.name != "id"
                # if f.blank is False and f.name not in ["id", "image"]
            ]
            missing_fields = [
                field for field in required_fields if field not in validated_data
            ]
            if missing_fields:
                raise ValidationError(
                    f"Missing fields for PUT request: {', '.join(missing_fields)}"
                )
            # 清空未在 validated_data 中提供的字段的值
            for field in Recipe._meta.fields:
                field_name = field.name
                if field_name not in validated_data and field_name not in [
                    "id",
                    # "tags",
                    # "ingredients",
                ]:
                    # print("field_name:", field_name) # field_name: image
                    default_value = field.default if field.has_default() else ""
                    setattr(instance, field_name, default_value)

                    """
                    if isinstance(field, models.FileField):
                        setattr(instance, field_name, None)
                    else:
                        default_value = field.default if field.has_default() else ""
                        setattr(instance, field_name, default_value)
                    """

            # 清空未在 validated_data 中提供的多对多字段
            for m2m_field in Recipe._meta.many_to_many:
                if m2m_field.name not in validated_data:
                    # 如果在 PUT 请求中未提供多对多字段，则清除它们 # 如果你再次查询该关系 .tags.all()，得到一个空的查询集（QuerySet）。
                    getattr(instance, m2m_field.name).clear()

        """Update recipe."""
        tags = validated_data.pop("tags", None)
        # print("tags:", tags)  #  tags: [OrderedDict([('name', 'recipe92')])]
        ingredients = validated_data.pop("ingredients", None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            """
            setattr(instance, attr, value) 是 Python 的內建方法，
            用於設置一個對象的屬性值。將 instance 的屬性 attr 設置為 value。
            validated_data = {
                "title": "New Recipe Title",
                "time_minutes": 45
            }
            將 instance 的 title 屬性設置為 "New Recipe Title"
            將 instance 的 time_minutes 屬性設置為 45
            """

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description", "image"]


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes."""

    class Meta:
        model = Recipe
        fields = ["id", "image"]
        read_only_fields = ["id"]
        extra_kwargs = {"image": {"required": "True"}}
        """
        模型層面（null=True）：允許在數據庫中存儲空值。
        序列化器層面（required=True）：在提交數據進行驗證時，
        該字段必須被提供。
        """
