from rest_framework import serializers


class ChatMessageSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=["system", "user", "assistant"])
    content = serializers.CharField(allow_blank=True)


class LLMInvokeSerializer(serializers.Serializer):
    messages = ChatMessageSerializer(many=True)
    max_tokens = serializers.IntegerField(required=False, min_value=1)
