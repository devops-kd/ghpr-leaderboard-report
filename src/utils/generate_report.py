def generate_report(summary):
    report = "Weekly Pull Request Summary:\n\n"
    for category, prs in summary.items():
        report += f"{category.capitalize()} ({len(prs)}):\n"
        for pr in prs:
            report += f"- {pr['title']} (URL: {pr['url']}, USER: {pr['user']}, CREATED_DATE: {pr['created_at']})\n"
    return report