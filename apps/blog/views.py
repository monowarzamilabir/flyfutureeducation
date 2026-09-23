from django.views.generic import DetailView, ListView

from .models import Category, Post


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        qs = Post.objects.filter(is_published=True)
        category_slug = self.kwargs.get("slug") if self.request.resolver_match.url_name == "category" else None
        tag_slug = self.kwargs.get("slug") if self.request.resolver_match.url_name == "tag" else None
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if tag_slug:
            qs = qs.filter(tags__slug=tag_slug)
        query = self.request.GET.get("q", "").strip()
        if query:
            qs = qs.filter(title__icontains=query)
        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all()
        ctx["query"] = self.request.GET.get("q", "")
        ctx["current_category"] = self.kwargs.get("slug") if self.request.resolver_match.url_name == "category" else None
        ctx["current_tag"] = self.kwargs.get("slug") if self.request.resolver_match.url_name == "tag" else None
        ctx["meta_title"] = "Blog, News & Events | Fly Future Education"
        ctx["meta_description"] = "Study-abroad tips, visa updates, scholarship news, and events from Fly Future Education."
        return ctx


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = ctx["post"]
        ctx["meta_title"] = post.meta_title or post.title
        ctx["meta_description"] = post.meta_description or post.excerpt
        ctx["related_posts"] = Post.objects.filter(is_published=True, category=post.category).exclude(pk=post.pk)[:3]
        return ctx
