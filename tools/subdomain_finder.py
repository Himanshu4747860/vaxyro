def run_subdomain_finder(domain):
  return [
      f"mail.{domain}",
      f"admin.{domain}",
      f"cdn.{domain}",
      f"blog.{domain}"
  ]