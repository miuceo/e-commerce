from rest_framework import serializers
from .models import Tag, Blog
from django.utils.text import slugify


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "tag")

    def validate_tag(self, value):
        if not value:
            raise serializers.ValidationError("Tag cannot be empty")
        if len(value) > 10:
            raise serializers.ValidationError("Tag cannot exceed 10 characters")
        qs = Tag.objects.filter(tag=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Tag must be unique")
        return value


class BlogSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        source="tags"
    )

    class Meta:
        model = Blog
        fields = [
            "slug", "title", "text", "quote", "author", "image",
            "tags", "tag_ids", "created_at", "updated_at"
        ]
        read_only_fields = ["slug", "created_at", "updated_at"]


    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title cannot be empty")
        if len(value) > 200:
            raise serializers.ValidationError("Title cannot exceed 200 characters")
        return value

    def validate_quote(self, value):
        if not value:
            raise serializers.ValidationError("Quote cannot be empty")
        if len(value) > 100:
            raise serializers.ValidationError("Quote cannot exceed 100 characters")
        return value

    def validate_author(self, value):
        if not value:
            raise serializers.ValidationError("Author cannot be empty")
        if len(value) > 100:
            raise serializers.ValidationError("Author cannot exceed 100 characters")
        return value

    def validate_text(self, value):
        if not value:
            raise serializers.ValidationError("Text cannot be empty")
        return value

    def validate_slug(self, value):
        if not value:
            value = slugify(self.initial_data.get("title", ""))
        qs = Blog.objects.filter(slug=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Slug must be unique")
        return value

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        if not validated_data.get("slug"):
            base_slug = slugify(validated_data.get("title", ""))
            slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            validated_data["slug"] = slug

        blog = Blog.objects.create(**validated_data)
        blog.tags.set(tags)
        return blog

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        if not validated_data.get("slug"):
            base_slug = slugify(validated_data.get("title", instance.title))
            slug = base_slug
            counter = 1
            qs = Blog.objects.exclude(pk=instance.pk)
            while qs.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            validated_data["slug"] = slug

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if tags is not None:
            instance.tags.set(tags)
        instance.save()
        return instance
